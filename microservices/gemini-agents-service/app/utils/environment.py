import os


RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)
QUEUE_NAME = os.getenv("GEMINI_MESSAGING_QUEUE_NAME", "gemini-messaging")

LOGGER_URL = os.getenv("LOGGER_URL", None)
LOGGER_TOKEN = os.getenv("LOGGER_TOKEN", None)
