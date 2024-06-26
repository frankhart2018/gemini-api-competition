from pydantic import BaseModel
from enum import Enum


class ChatState(Enum):
    DUMP = "DUMP"


class ChatRequest(BaseModel):
    state: ChatState
    chat_id: str
    message: str
    sender_id: str

    class Config:
        use_enum_values = True
