import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
import pika
from pika.adapters.blocking_connection import BlockingChannel
import argparse
from argparse import Namespace
import json
from typing import Optional

import pika.adapters.blocking_connection

from constants import GEMINI_MODEL
from environment import RABBIT_HOST, RABBIT_PORT, QUEUE_NAME


model: Optional[genai.GenerativeModel] = None


def prompt(model: genai.GenerativeModel, message: str) -> GenerateContentResponse:
    message_formatted = {"role": "user", "parts": [message]}

    return model.generate_content(message_formatted)


def message_processor(ch, method, _properties, body):
    global model

    body_decoded = json.loads(body.decode())
    message = body_decoded["input"]

    response = prompt(model=model, message=message)
    print(f"You: {message}")
    print(f"Gemini: {response.text}")  # Replace this with mongo insert call

    ch.basic_ack(delivery_tag=method.delivery_tag)


def init_model(api_key: str) -> genai.GenerativeModel:
    global model

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=GEMINI_MODEL)


def consume_queue() -> BlockingChannel:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT)
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=message_processor)

    channel.start_consuming()
    return channel


def main(args: Namespace):
    init_model(args.gemini_api_key)

    channel = None
    try:
        channel = consume_queue()
    except KeyboardInterrupt:
        if channel:
            channel.stop_consuming()
            channel.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Gemini executor")
    parser.add_argument("--gemini-api-key", required=True, help="Gemini API key")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main(args=parse_args())
