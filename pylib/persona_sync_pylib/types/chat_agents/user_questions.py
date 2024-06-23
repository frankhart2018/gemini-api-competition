from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class UserQuestionState(Enum):
    PENDING = "PENDING"
    ANSWERED = "ANSWERED"
    REJECTED = "REJECTED"


class UserQuestion(BaseModel):
    user_id: str
    question: str
    question_embedding: List[float]
    question_id: str
    interaction_id: str
    state: Optional[UserQuestionState] = UserQuestionState.PENDING
    answer: Optional[str] = ""

    class Config:
        use_enum_values = True
