import pika

from app.utils.environment import RABBIT_HOST, RABBIT_PORT, QUEUE_NAME
from app.utils.logger import Logger, LogLevel


def publish_message(message: str) -> bool:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    publish_status = False
    try:
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        publish_status = True
    except Exception as e:
        Logger().log(LogLevel.ERROR, f"Failed to publish message: {e}")
    finally:
        connection.close()

    return publish_status
