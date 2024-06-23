from pydantic import BaseModel
from typing import List
from enum import Enum


class UserMatchingState(Enum):
    INDEX = "INDEX"
    MATCH = "MATCH"


class UserEntry(BaseModel):
    user_id: str
    user_summary_embedding: List[float]


class UserEntryQueueRequest(UserEntry):
    state: UserMatchingState

    class Config:
        use_enum_values = True
