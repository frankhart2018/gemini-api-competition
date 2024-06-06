import pika
from pika.adapters.blocking_connection import BlockingChannel
import json
import pydantic
from typing import Optional, Union

from ..singleton import singleton
from ..environment import QUEUE_NAME, RABBIT_HOST, RABBIT_PORT
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest
from ..logger import Logger, LogLevel
from ..handler_factory import prompt_handler_factory


@singleton
class Consumer:
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__channel = self.__init_channel()
        self.__model = model

    def start_listening(self) -> None:
        self.__channel.start_consuming()

    def stop_listening(self) -> None:
        self.__channel.stop_consuming()
        self.__channel.close()

    def __init_channel(self) -> BlockingChannel:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
        )
        channel = connection.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=QUEUE_NAME, on_message_callback=self.message_processor
        )

        return channel

    def message_processor(self, ch, method, _properties, body):
        body_decoded = json.loads(body.decode())

        request: Optional[Union[QueueRequest, StateMachineQueueRequest]] = None
        try:
            request = StateMachineQueueRequest(**body_decoded)
        except pydantic.ValidationError as pe:
            try:
                request = QueueRequest(**body_decoded)
            except pydantic.ValidationError:
                Logger().log(
                    log_level=LogLevel.ERROR, message=f"Invalid message: {body}"
                )
                # At this point the request is unprocessable
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

        if request:
            handler = prompt_handler_factory(state=request.state, model=self.__model)
            response = handler.execute(request)

            if response:
                handler.transition(prompt_request=request, model_output=response)

            ch.basic_ack(delivery_tag=method.delivery_tag)
