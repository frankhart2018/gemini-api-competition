import os


USER_MATCHING_COLLECTION = os.getenv("USER_MATCHING_COLLECTION", "user-matching")

NUM_MATCHES = int(os.getenv("NUM_MATCHES", 5))

QUEUE_NAME = os.getenv("QUEUE_NAME", "user-matching-queue")
