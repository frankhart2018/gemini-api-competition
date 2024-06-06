from pydantic import BaseModel
from typing import List

from app.model.common import QAndA
from app.model.initiate_request import InitiateChatRabbitRequest


class RevertChatHTTPRequest(BaseModel):
    q_and_a_s: List[QAndA]


class RevertChatRabbitRequest(InitiateChatRabbitRequest):
    pass
