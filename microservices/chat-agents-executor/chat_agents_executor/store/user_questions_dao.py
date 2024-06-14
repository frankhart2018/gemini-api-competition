from pymongo.results import InsertOneResult
import json
from typing import List
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.mongo_ops import MongoCollection
from persona_sync_pylib.types.chat_agents import UserQuestion, UserQuestionState

from ..utils.environment import MONGO_DB_NAME, USER_QUESTIONS_COLLECTION


@singleton
class UserQuestionsDao:
    def __init__(self) -> None:
        self.__collection = MongoCollection(db_name=MONGO_DB_NAME).get_collection(
            USER_QUESTIONS_COLLECTION
        )

    def insert(self, user_question: UserQuestion) -> InsertOneResult:
        return self.__collection.insert_one(json.loads(user_question.model_dump_json()))

    def find_questions_for_user(self, user_id: str) -> List[UserQuestion]:
        user_questions = self.__collection.find_one(
            {
                "user_id": user_id,
                "state": {
                    "$in": [
                        UserQuestionState.ANSWERED.value,
                        UserQuestionState.REJECTED.value,
                    ]
                },
            }
        )
        if user_questions:
            return [UserQuestion(**user_question) for user_question in user_questions]
        return []
