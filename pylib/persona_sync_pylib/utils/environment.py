import os


RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT = os.getenv("RABBIT_PORT", 5672)
RABBIT_CONNECTION_ATTEMPTS = os.getenv("RABBIT_CONNECTION_ATTEMPTS", 5)
RABBIT_CONNECTION_DELAY = os.getenv("RABBIT_CONNECTION_DELAY", 3)

LOGGER_URL = os.getenv("LOGGER_URL", None)
LOGGER_TOKEN = os.getenv("LOGGER_TOKEN", None)

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb://localhost:27017/")
MILVUS_HOST = os.getenv("MILVUS_HOST", "http://localhost:19530/")

EMBEDDING_SIZE = int(os.getenv("EMBEDDING_SIZE", 768))

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
