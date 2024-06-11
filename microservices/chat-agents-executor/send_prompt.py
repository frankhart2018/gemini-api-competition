# JUST FOR LOCAL TESTING, DO NOT DEPLOY

import argparse
import pika
from bson import ObjectId
from persona_sync_pylib.types.chat_agents import QueueRequest, StateMachineQueueRequest
from persona_sync_pylib.queue import publish_chat_agents_message

from chat_agents_executor.store.prompt_input_dao import PromptInputDao
from chat_agents_executor.utils.environment import QUEUE_NAME


def main():
    parser = argparse.ArgumentParser(description="Send prompt to chat-agents")
    parser.add_argument("message", type=str, help="Message to send to chat-agents")

    args = parser.parse_args()

    if ObjectId.is_valid(args.message):
        message = PromptInputDao().get_prompt_input(prompt_id=args.message)
    else:
        message = StateMachineQueueRequest(
            input=args.message,
            state="COMMENCE",
            u1_uid="1",
            u2_uid="2",
            u1_summary="This individual is a passionate programmer who enjoys coding and is currently learning C++. They find solace in watching movies and enjoying good food during their free time.  Their ultimate dream would be to code all day long, showcasing their dedication to the field. They are proud of the programs they have created, suggesting a strong work ethic and a desire for continuous learning.",
            u2_summary="This person is passionate about cooking and has a desire to learn how to play the flute. They are proud of climbing Mount Everest, a significant accomplishment. While they are not particularly fond of books, movies, or art, they are interested in traveling to Japan to see Mount Fuji.",
            target="u1",
        )

        res = PromptInputDao().upsert(prompt_input=message)
        message.interaction_id = str(res.upserted_id)

    publish_chat_agents_message(message=message, queue_name=QUEUE_NAME)


if __name__ == "__main__":
    main()
