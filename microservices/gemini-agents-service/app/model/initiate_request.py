from pydantic import BaseModel
from typing import List, Optional

from app.model.prompt_request import PromptRabbitRequest
from app.model.common import QAndA


class InitiateChatHTTPRequest(BaseModel):
    u1_uid: str
    u2_uid: str
    u1_summary: str
    u2_summary: str


class InitiateChatRabbitRequest(PromptRabbitRequest):
    u1_uid: str
    u2_uid: str
    u1_summary: str
    u2_summary: str
    target: str
    q_and_a_s: Optional[List[QAndA]] = []
    previous_response: Optional[str] = ""
    interaction_id: Optional[str] = ""
    interaction_length: Optional[int] = 0
