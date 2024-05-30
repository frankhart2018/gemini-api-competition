import pika
from pika.adapters.blocking_connection import BlockingChannel
import json

from singleton import singleton
from environment import QUEUE_NAME, RABBIT_HOST, RABBIT_PORT
from gemini import GeminiAPIDao


@singleton
class QueueListener:
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
        message = body_decoded["input"]

        response = self.__model.prompt(message=message)
        print(f"You: {message}")
        print(f"Gemini: {response}")  # Replace this with mongo insert call

        ch.basic_ack(delivery_tag=method.delivery_tag)
