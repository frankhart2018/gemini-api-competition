import os


QUEUE_NAME = os.getenv("GEMINI_MESSAGING_QUEUE_NAME", "gemini-messaging")

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "chat-agents")
PROMPT_INPUTS_COLLECTION = os.getenv("PROMPT_INPUTS_COLLECTION", "prompt-inputs")
