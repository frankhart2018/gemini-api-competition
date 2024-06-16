import os


USER_MATCHING_COLLECTION = os.getenv("USER_MATCHING_COLLECTION", "user-matching")

NUM_MATCHES = int(os.getenv("NUM_MATCHES", 5))

QUEUE_NAME = os.getenv("QUEUE_NAME", "user-matching-queue")

BLOOMD_HOST = os.getenv("BLOOMD_HOST", "localhost")
BLOOMD_PORT = int(os.getenv("BLOOMD_PORT", 8673))
BLOOMD_TIMEOUT = int(os.getenv("BLOOMD_TIMEOUT", 5))
BLOOMD_FILTER_NAME = os.getenv("BLOOMD_FILTER_NAME", "matched-users")
BLOOMD_CAPACITY = int(os.getenv("BLOOMD_CAPACITY", 10_000_000))
BLOOMD_PROBABILITY = float(os.getenv("BLOOMD_PROBABILITY", 0.001))
