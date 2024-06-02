from pydantic import BaseModel, field_validator
from enum import Enum
from typing import Optional


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


class StateMachineQueueRequest(QueueRequest):
    from_uid: str
    to_uid: str
    u1_summary: str
    u2_summary: str
    target: str
    questions: Optional[str] = ""
    previous_response: Optional[str] = ""
    interaction_id: Optional[str] = ""
