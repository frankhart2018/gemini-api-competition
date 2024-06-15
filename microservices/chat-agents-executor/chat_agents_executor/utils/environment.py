import os


QUEUE_NAME = os.getenv("GEMINI_MESSAGING_QUEUE_NAME", "gemini-messaging")

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "chat-agents")
PROMPT_INPUTS_COLLECTION = os.getenv("PROMPT_INPUTS_COLLECTION", "prompt-inputs")
USER_QUESTIONS_COLLECTION = os.getenv("USER_QUESTIONS_COLLECTION", "user-questions")
VAL_EMBEDDINGS_COLLECTION = os.getenv("VAL_EMBEDDINGS_COLLECTION", "val-embeddings")

MAX_INTERACTIONS = os.getenv("MAX_INTERACTIONS", 4)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
EMBED_MODEL = os.getenv("EMBED_MODEL", "models/embedding-001")
