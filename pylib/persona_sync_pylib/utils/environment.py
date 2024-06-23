import os


RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)

LOGGER_URL = os.getenv("LOGGER_URL", None)
LOGGER_TOKEN = os.getenv("LOGGER_TOKEN", None)

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb://localhost:27017/")
MILVUS_HOST = os.getenv("MILVUS_HOST", "http://localhost:19530/")

EMBEDDING_SIZE = int(os.getenv("EMBEDDING_SIZE", 768))
