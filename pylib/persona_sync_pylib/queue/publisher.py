import pika
from pydantic import BaseModel

from persona_sync_pylib.utils.environment import RABBIT_HOST, RABBIT_PORT
from persona_sync_pylib.utils.logger import Logger, LogLevel


def publish_message(message: BaseModel, queue_name: str) -> bool:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    )
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
