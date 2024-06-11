from pydantic import BaseModel
from typing import List
from persona_sync_pylib.types.chat_agents import QAndA, StateMachineQueueRequest


class RevertChatHTTPRequest(BaseModel):
    q_and_a_s: List[QAndA]


class RevertChatRabbitRequest(StateMachineQueueRequest):
    pass
