from pydantic import BaseModel, field_validator
from enum import Enum
from typing import Optional, List


class PromptState(Enum):
    # States of chat agents state machine
    COMMENCE = "COMMENCE"
    COMMUNICATE = "COMMUNICATE"
    ASK_GEMINI = "ASK_GEMINI"
    ASK_USER = "ASK_USER"
    TERMINAL = "TERMINAL"

    # Singular prompt, not part of chat agents
    PROMPT = "PROMPT"


class QueueRequest(BaseModel):
    input: str
    state: PromptState

    class Config:
        use_enum_values = True


class QAndA(BaseModel):
    question: str
    answer: Optional[str] = ""


class StateMachineQueueRequest(QueueRequest):
    u1_uid: str
    u2_uid: str
    u1_summary: str
    u2_summary: str
    target: str
    q_and_a_s: Optional[List[QAndA]] = []
    previous_response: Optional[str] = ""
    interaction_id: Optional[str] = ""
    interaction_length: Optional[int] = 0
