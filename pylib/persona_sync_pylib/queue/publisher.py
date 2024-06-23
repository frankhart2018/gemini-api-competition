import pika
import pika.exceptions
from pydantic import BaseModel

from persona_sync_pylib.utils.environment import (
    RABBIT_HOST,
    RABBIT_PORT,
    RABBIT_CONNECTION_ATTEMPTS,
    RABBIT_CONNECTION_DELAY,
)
from persona_sync_pylib.utils.logger import Logger, LogLevel


def publish_message(message: BaseModel, queue_name: str) -> bool:
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
        return False

    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message.model_dump_json(),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
    except Exception as e:
        Logger().log(LogLevel.ERROR, f"Failed to publish message: {e}")
        return False

    connection.close()
    return True
