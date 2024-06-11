from pymongo.results import InsertOneResult
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.mongo_ops import MongoCollection
from persona_sync_pylib.types.chat_agents import UserQuestion

from ..utils.environment import MONGO_DB_NAME, USER_QUESTIONS_COLLECTION


@singleton
class UserQuestionsDao:
    def __init__(self) -> None:
        self.__collection = MongoCollection(db_name=MONGO_DB_NAME).get_collection(
            USER_QUESTIONS_COLLECTION
        )

    def insert(self, user_question: UserQuestion) -> InsertOneResult:
        return self.__collection.insert_one(user_question.model_dump())
