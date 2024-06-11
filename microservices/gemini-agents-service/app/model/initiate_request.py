from pydantic import BaseModel
from persona_sync_pylib.types.chat_agents import StateMachineQueueRequest

from app.model.prompt_request import PromptRabbitRequest


class InitiateChatHTTPRequest(BaseModel):
    u1_uid: str
    u2_uid: str
    u1_summary: str
    u2_summary: str


class InitiateChatRabbitRequest(StateMachineQueueRequest):
    pass
