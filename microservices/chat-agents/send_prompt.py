# JUST FOR LOCAL TESTING, DO NOT DEPLOY

import pika
import json
import argparse

from environment import RABBIT_HOST, RABBIT_PORT, QUEUE_NAME


def main():
    parser = argparse.ArgumentParser(description="Send prompt to chat-agents")
    parser.add_argument("message", type=str, help="Message to send to chat-agents")

    args = parser.parse_args()

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    message = json.dumps({"input": args.message, "state": "PROMPT"})
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )
    print(f" [x] Sent '{message}'")
    connection.close()


if __name__ == "__main__":
    main()
