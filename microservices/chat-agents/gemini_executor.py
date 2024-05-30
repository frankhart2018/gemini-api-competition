import argparse
from argparse import Namespace
from typing import Optional


from gemini import GeminiAPIDao
from queue_listener import QueueListener


def main(args: Namespace):
    model = GeminiAPIDao(api_key=args.gemini_api_key)
    queue_listener = QueueListener(model)

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
