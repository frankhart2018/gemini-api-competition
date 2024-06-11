import argparse
from argparse import Namespace

from chat_agents_executor.utils.gemini import GeminiAPIDao
from chat_agents_executor.queue import ChatAgentsConsumer


def main(args: Namespace):
    model = GeminiAPIDao(api_key=args.gemini_api_key)
    queue_listener = ChatAgentsConsumer(model=model)

    try:
        queue_listener.start_listening()
    except KeyboardInterrupt:
        queue_listener.stop_listening()


def parse_args():
    parser = argparse.ArgumentParser(description="Gemini executor")
    parser.add_argument("--gemini-api-key", required=True, help="Gemini API key")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main(args=parse_args())
