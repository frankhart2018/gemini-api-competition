import json
from typing import Optional
import pydantic
import websockets
from persona_sync_pylib.queue.consumer import Consumer
from persona_sync_pylib.types.user_chat_system import ChatState, ChatRequest
from persona_sync_pylib.utils.logger import Logger, LogLevel

from ..utils.environment import QUEUE_NAME
from ..store.chat_socket_dao import ChatSocketDao
from ..store.chat_history_dao import ChatHistoryDao


class UserChatConsumer(Consumer):
    def __init__(self) -> None:
        super().__init__(queue_name=QUEUE_NAME)
        self.__chat_socket_dao = ChatSocketDao()

    def __handle_socket_send(self, chat_request: ChatRequest) -> None:
        socket_sessions = self.__chat_socket_dao.get_socket_sessions(
            chat_request.chat_id
        )

        if not socket_sessions:
            Logger.log(
                log_level=LogLevel.ERROR,
                message=f"Socket sessions not found for chat_id: {chat_request.chat_id}",
            )
            return

        sessions = [
            session
            for uid, session in socket_sessions.items()
            if uid != chat_request.sender_id
        ]
        websockets.broadcast(sessions, chat_request.model_dump_json(exclude={"state"}))

    def __handle_dump(self, chat_request: ChatRequest) -> None:
        ChatHistoryDao().upsert_chat(chat_request)

    def message_processor(self, ch, method, _properties, body):
        body_decoded = json.loads(body.decode())

        chat_request: Optional[ChatRequest] = None
        try:
            chat_request = ChatRequest(**body_decoded)
        except pydantic.ValidationError as e:
            Logger.log(
                log_level=LogLevel.ERROR,
                message=f"Error while parsing chat request: {e}",
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if chat_request:
            match chat_request.state:
                case ChatState.SOCKET_SEND:
                    self.__handle_socket_send(chat_request)
                case ChatState.DUMP:
                    self.__handle_dump(chat_request)
        ch.basic_ack(delivery_tag=method.delivery_tag)
