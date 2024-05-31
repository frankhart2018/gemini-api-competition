import os


QUEUE_NAME = os.getenv("GEMINI_MESSAGING_QUEUE_NAME", "gemini-messaging")
RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)

LOGGER_URL = os.getenv("LOGGER_URL", None)
LOGGER_TOKEN = os.getenv("LOGGER_TOKEN", None)
