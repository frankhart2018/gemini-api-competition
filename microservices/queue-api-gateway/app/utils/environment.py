import os


CHAT_AGENTS_QUEUE = os.getenv("GEMINI_MESSAGING_QUEUE_NAME", "gemini-messaging")
USER_CHAT_QUEUE = os.getenv("USER_CHAT_QUEUE_NAME", "user-chat-system")

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "chat-agents")
PROMPT_INPUTS_COLLECTION = os.getenv("PROMPT_INPUTS_COLLECTION", "prompt-inputs")

SOCKET_SESSIONS_BUCKET = os.getenv("SOCKET_SESSIONS_BUCKET", "socket_sessions")
SOCKET_SESSIONS_TMP_DIR = os.getenv("SOCKET_SESSIONS_TMP_DIR", "/tmp/socket_sessions")
