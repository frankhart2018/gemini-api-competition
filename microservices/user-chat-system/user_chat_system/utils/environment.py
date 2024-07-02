import os


QUEUE_NAME = os.getenv("CHAT_SYSTEM_QUEUE_NAME", "user-chat-system")

SOCKET_SESSIONS_BUCKET = os.getenv("SOCKET_SESSIONS_BUCKET", "socket_sessions")
SOCKET_SESSIONS_TMP_DIR = os.getenv("SOCKET_SESSIONS_TMP_DIR", "/tmp/socket_sessions")

CHAT_HISTORY_DB = os.getenv("CHAT_HISTORY_DB", "chat_history")
CHAT_HISTORY_COLLECTION = os.getenv("CHAT_HISTORY_COLLECTION", "chats")
