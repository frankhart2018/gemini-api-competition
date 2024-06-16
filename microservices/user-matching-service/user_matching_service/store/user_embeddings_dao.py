from typing import Any, Dict, List
import numpy as np
from persona_sync_pylib.utils.milvus_ops import MilvusConnection
from persona_sync_pylib.types.user_matching import UserEntry
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.user_matching import UserEntry

from ..utils.environment import USER_MATCHING_COLLECTION, NUM_MATCHES


@singleton
class UserEmbeddingsDao:
    def __init__(self) -> None:
        self.__client = MilvusConnection(
            collection_name=USER_MATCHING_COLLECTION
        ).get_client()

    def __get_embedding_as_array(self, user_entry: UserEntry) -> Dict[str, Any]:
        return {
            "user_id": user_entry.user_id,
            "user_summary_embedding": np.array(user_entry.user_summary_embedding),
        }

    def upsert(self, user_entry: UserEntry) -> None:
        self.__client.upsert(
            collection_name=USER_MATCHING_COLLECTION,
            data=[self.__get_embedding_as_array(user_entry)],
        )

    def search(self, user_entry: UserEntry) -> List[UserEntry]:
        matches = self.__client.search(
            collection_name=USER_MATCHING_COLLECTION,
            query_vector=np.array(user_entry.user_summary_embedding),
            limit=NUM_MATCHES,
        )

        match_entities = [UserEntry(**match["entity"]) for match in matches]
        return match_entities
