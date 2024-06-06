import pymongo
from pymongo.collection import Collection
from typing import List, Dict, Any
from bson.objectid import ObjectId

from app.utils.singleton import singleton
from app.utils.environment import MONGO_HOST
from app.utils.constants import MONGO_DB_NAME, PROMPT_INPUTS_COLLECTION
from app.model.common import QAndA


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

    def update_questions_answers(
        self, interaction_id: str, q_and_a_s: List[QAndA]
    ) -> Dict[str, Any]:
        return self.__collection.find_one_and_update(
            {"_id": ObjectId(interaction_id)},
            {"$set": {"q_and_a_s": q_and_a_s}},
            return_document=True,
        )
