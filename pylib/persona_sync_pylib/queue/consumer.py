import pika
from pika.adapters.blocking_connection import BlockingChannel
import pika.exceptions

from persona_sync_pylib.utils.environment import (
    RABBIT_HOST,
    RABBIT_PORT,
    RABBIT_CONNECTION_ATTEMPTS,
    RABBIT_CONNECTION_DELAY,
)
from persona_sync_pylib.utils.logger import Logger, LogLevel


class Consumer:
    def __init__(self, queue_name: str) -> None:
        self.__channel = self.__init_channel(queue_name=queue_name)

    def start_listening(self) -> None:
        self.__channel.start_consuming()

    def stop_listening(self) -> None:
        self.__channel.stop_consuming()
        self.__channel.close()

    def __init_channel(self, queue_name: str) -> BlockingChannel:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    port=RABBIT_PORT,
                    connection_attempts=RABBIT_CONNECTION_ATTEMPTS,
                    retry_delay=RABBIT_CONNECTION_DELAY,
                )
            )
        except pika.exceptions.AMQPConnectionError as e:
            Logger.log(
                LogLevel.ERROR,
                f"Failed to connect to RabbitMQ: {e}",
            )
            raise Exception(f"Failed to connect to RabbitMQ: {e}")

        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=queue_name, on_message_callback=self.message_processor
        )

        return channel

    def message_processor(self, ch, method, _properties, body):
        pass
