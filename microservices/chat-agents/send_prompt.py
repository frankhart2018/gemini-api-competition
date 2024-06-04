# JUST FOR LOCAL TESTING, DO NOT DEPLOY

import argparse
import pika

from chat_agents.mongo_ops import PromptInputDao
from chat_agents.prompt_inputs import QueueRequest, StateMachineQueueRequest
from chat_agents.environment import RABBIT_HOST, RABBIT_PORT, QUEUE_NAME


def main():
    parser = argparse.ArgumentParser(description="Send prompt to chat-agents")
    parser.add_argument("message", type=str, help="Message to send to chat-agents")

    args = parser.parse_args()

    message = StateMachineQueueRequest(
        input=args.message,
        state="COMMENCE",
        from_uid="1",
        to_uid="2",
        u1_summary="This individual is a passionate programmer who enjoys coding and is currently learning C++. They find solace in watching movies and enjoying good food during their free time.  Their ultimate dream would be to code all day long, showcasing their dedication to the field. They are proud of the programs they have created, suggesting a strong work ethic and a desire for continuous learning.",
        u2_summary="This person is passionate about cooking and has a desire to learn how to play the flute. They are proud of climbing Mount Everest, a significant accomplishment. While they are not particularly fond of books, movies, or art, they are interested in traveling to Japan to see Mount Fuji.",
        target="u1",
    )

    res = PromptInputDao().upsert(prompt_input=message)
    message.interaction_id = str(res.upserted_id)

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
        print(e)

    connection.close()


if __name__ == "__main__":
    main()
