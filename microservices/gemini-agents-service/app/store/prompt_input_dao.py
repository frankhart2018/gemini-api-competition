from typing import Any, Dict, List, Optional, Union
import pydantic
from bson.objectid import ObjectId
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.mongo_ops import MongoCollection
from persona_sync_pylib.types.chat_agents import (
    QAndA,
    QueueRequest,
    StateMachineQueueRequest,
)

from app.utils.environment import MONGO_DB_NAME, PROMPT_INPUTS_COLLECTION


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

    def get_prompt_input(
        self, prompt_id: str
    ) -> Optional[Union[QueueRequest, StateMachineQueueRequest]]:
        result = self.__collection.find_one({"_id": ObjectId(prompt_id)})
        if result is None:
            return None

        try:
            return StateMachineQueueRequest(**result)
        except pydantic.ValidationError as pe:
            try:
                return QueueRequest(**result)
            except pydantic.ValidationError:
                return None
