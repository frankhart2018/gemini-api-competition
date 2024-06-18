import json
import pydantic
from typing import Optional
from persona_sync_pylib.queue import Consumer, publish_message
from persona_sync_pylib.types.user_matching import (
    UserEntryQueueRequest,
    UserMatchingState,
    UserEntry,
)
from persona_sync_pylib.utils.logger import Logger, LogLevel
from persona_sync_pylib.utils.singleton import singleton

from ..utils.environment import QUEUE_NAME, BLOOMD_FILTER_NAME
from ..store.user_embeddings_dao import UserEmbeddingsDao
from ..store.match_filter_dao import MatchFilterDAO


@singleton
class UserMatchingConsumer(Consumer):
    def __init__(self) -> None:
        super().__init__(queue_name=QUEUE_NAME)

    def __handle_index_state(self, user_entry: UserEntryQueueRequest) -> None:
        UserEmbeddingsDao().upsert(
            user_entry=UserEntry(
                user_id=user_entry.user_id,
                user_summary_embedding=user_entry.user_summary_embedding,
            )
        )

        forward_request = user_entry.model_copy(deep=True)
        forward_request.state = UserMatchingState.MATCH
        publish_message(message=forward_request, queue_name=QUEUE_NAME)

    def __handle_match_state(self, user_entry: UserEntryQueueRequest) -> None:
        matches = UserEmbeddingsDao().search(
            user_entry=UserEntry(
                user_id=user_entry.user_id,
                user_summary_embedding=user_entry.user_summary_embedding,
            )
        )

        self_user_id = user_entry.user_id
        filter = MatchFilterDAO().get_filter()
        for match in matches:
            user_id = match.user_id
            filter.set(filter_name=BLOOMD_FILTER_NAME, key=f"{self_user_id}-{user_id}")

    def message_processor(self, ch, method, _properties, body):
        body_decoded = json.loads(body.decode())

        user_entry: Optional[UserEntryQueueRequest] = None
        try:
            user_entry = UserEntryQueueRequest(**body_decoded)
        except pydantic.ValidationError as pe:
            Logger().log(
                log_level=LogLevel.ERROR,
                message=f"Invalid message received: {pe}",
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if user_entry:
            match user_entry.state:
                case UserMatchingState.INDEX:
                    self.__handle_index_state(user_entry)
                case UserMatchingState.MATCH:
                    self.__handle_match_state(user_entry)

            ch.basic_ack(delivery_tag=method.delivery_tag)
