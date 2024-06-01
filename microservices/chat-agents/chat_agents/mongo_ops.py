import pymongo
from pymongo.collection import Collection
from pymongo.results import UpdateResult
from typing import Union, Optional
from bson.objectid import ObjectId

from .singleton import singleton
from .environment import MONGO_HOST
from .prompt_inputs import QueueRequest, StateMachineQueueRequest
from .constants import MONGO_DB_NAME, PROMPT_INPUTS_COLLECTION


@singleton
class MongoCollection:
    def __init__(self, db_name: str) -> None:
        client = pymongo.MongoClient(host=MONGO_HOST)
        self.__db = client[db_name]

    def get_collection(self, collection: str) -> Collection:
        return self.__db[collection]


@singleton
class PromptInputDao:
    def __init__(self) -> None:
        self.__collection = MongoCollection(db_name=MONGO_DB_NAME).get_collection(
            PROMPT_INPUTS_COLLECTION
        )

    def upsert(
        self,
        prompt_input: Union[QueueRequest, StateMachineQueueRequest],
        prompt_id: Optional[str] = None,
    ) -> UpdateResult:
        if prompt_id is None:
            prompt_id = ObjectId()

        return self.__collection.update_one(
            {"_id": prompt_id}, {"$set": prompt_input.model_dump()}, upsert=True
        )
