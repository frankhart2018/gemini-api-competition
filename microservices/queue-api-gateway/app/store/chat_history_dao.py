from persona_sync_pylib.utils.mongo_ops import MongoCollection
from persona_sync_pylib.types.user_chat_system import ChatRequest
from persona_sync_pylib.utils.singleton import singleton

from ..utils.environment import CHAT_HISTORY_DB, CHAT_HISTORY_COLLECTION


@singleton
class ChatHistoryDao:
    def __init__(self) -> None:
        self.__collection = MongoCollection(db_name=CHAT_HISTORY_DB).get_collection(
            collection=CHAT_HISTORY_COLLECTION
        )

    def get_chat(self, chat_id: str, limit: int) -> list:
        result = self.__collection.find_one(
            {"chat_id": chat_id},
            {"_id": 0, "messages": {"$slice": -limit}},
        )

        return result
