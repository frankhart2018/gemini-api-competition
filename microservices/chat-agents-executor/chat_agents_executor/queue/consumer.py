import json
import pydantic
from typing import Optional, Union
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.chat_agents import QueueRequest, StateMachineQueueRequest
from persona_sync_pylib.utils.logger import Logger, LogLevel
from persona_sync_pylib.queue import Consumer

from ..gemini import GeminiAPIDao
from ..handler_factory import prompt_handler_factory


@singleton
class ChatAgentsConsumer(Consumer):
    def __init__(self, model: GeminiAPIDao) -> None:
        super().__init__()
        self.__model = model

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
