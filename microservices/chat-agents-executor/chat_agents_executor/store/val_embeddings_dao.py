from pymongo.results import InsertOneResult
import json
from typing import Optional
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.mongo_ops import MongoCollection
from persona_sync_pylib.types.chat_agents import ValEmbeddings

from ..utils.environment import MONGO_DB_NAME, VAL_EMBEDDINGS_COLLECTION


@singleton
class ValEmbeddingsDao:
    def __init__(self) -> None:
        self.__collection = MongoCollection(db_name=MONGO_DB_NAME).get_collection(
            VAL_EMBEDDINGS_COLLECTION
        )

    def upsert(self, val_embedding: ValEmbeddings, tracking_id: str) -> InsertOneResult:
        return self.__collection.update_one(
            {"_id": tracking_id},
            {"$set": val_embedding.model_dump()},
            upsert=True,
        )
