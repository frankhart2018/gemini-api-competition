from fastapi import WebSocket, APIRouter
from fastapi.exceptions import HTTPException
import starlette
from collections import defaultdict
from persona_sync_pylib.queue.publisher import publish_message
from persona_sync_pylib.types.user_chat_system import ChatRequest, ChatState

from ..utils.environment import USER_CHAT_QUEUE
from ..store.chat_history_dao import ChatHistoryDao


router = APIRouter()
ROOMS = defaultdict(dict)


@router.websocket("/chat")
async def chat_endpoint(websocket: WebSocket, chat_id: str, user_id: str):
    await websocket.accept()
    ROOMS[chat_id][user_id] = websocket

    while True:
        try:
            data = await websocket.receive_text()

            chat_request = ChatRequest(
                state=ChatState.DUMP,
                chat_id=chat_id,
                sender_id=user_id,
                message=data,
            )
            publish_message(message=chat_request, queue_name=USER_CHAT_QUEUE)

            broadcast_sockets = [
                socket for uid, socket in ROOMS[chat_id].items() if uid != user_id
            ]
            for socket in broadcast_sockets:
                await socket.send_text(data)
        except starlette.websockets.WebSocketDisconnect:
            del ROOMS[chat_id][user_id]
            break


@router.get("/chat/{chat_id}")
async def get_chat(chat_id: str):
    result = ChatHistoryDao().get_chat(chat_id=chat_id, limit=10)

    if result:
        return result
    return HTTPException(status_code=404, detail="Chat not found")
