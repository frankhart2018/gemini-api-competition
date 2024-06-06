from typing import Union
import pika

from ..prompt_inputs import QueueRequest, StateMachineQueueRequest
from ..environment import RABBIT_HOST, RABBIT_PORT, QUEUE_NAME
from ..logger import Logger, LogLevel


def publish_message(message: Union[QueueRequest, StateMachineQueueRequest]) -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message.model_dump_json(),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
    except Exception as e:
        Logger().log(LogLevel.ERROR, f"Failed to publish message: {e}")

    connection.close()
