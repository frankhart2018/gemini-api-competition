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

    def upsert_chat(self, chat_request: ChatRequest) -> None:
        self.__collection.update_one(
            {"chat_id": chat_request.chat_id},
            {
                "$push": {
                    "messages": chat_request.model_dump(exclude={"chat_id", "state"})
                }
            },
            upsert=True,
        )
