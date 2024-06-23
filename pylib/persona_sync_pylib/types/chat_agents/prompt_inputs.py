from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from bson.objectid import ObjectId


class PromptState(Enum):
    # States of chat agents state machine
    COMMENCE = "COMMENCE"
    COMMUNICATE = "COMMUNICATE"
    ASK_GEMINI = "ASK_GEMINI"
    ASK_USER = "ASK_USER"
    TERMINAL = "TERMINAL"

    # Singular prompt, not part of chat agents
    PROMPT = "PROMPT"

    # Singular embedding state, not part of chat agents
    EMBED = "EMBED"


class QueueRequest(BaseModel):
    input: str
    state: PromptState
    interaction_id: Optional[str] = ""
    previous_response: Optional[str] = ""

    class Config:
        use_enum_values = True


class QAndA(BaseModel):
    question: str
    answer: Optional[str] = ""
    obj_id: Optional[str] = str(ObjectId())


class StateMachineQueueRequest(QueueRequest):
    u1_uid: str
    u2_uid: str
    u1_summary: str
    u2_summary: str
    target: str
    q_and_a_s: Optional[List[QAndA]] = []
    interaction_length: Optional[int] = 0
