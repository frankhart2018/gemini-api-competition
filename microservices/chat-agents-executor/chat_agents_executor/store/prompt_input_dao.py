from typing import Any, Dict, List, Optional, Union
from pymongo.results import UpdateResult
from bson.objectid import ObjectId
import pydantic
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.environment import MONGO_DB_NAME, PROMPT_INPUTS_COLLECTION
from persona_sync_pylib.utils.mongo_ops import MongoCollection
from persona_sync_pylib.types.chat_agents import QueueRequest, StateMachineQueueRequest


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
            {"_id": ObjectId(prompt_id)},
            {"$set": prompt_input.model_dump()},
            upsert=True,
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
