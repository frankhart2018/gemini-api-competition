from pydantic import BaseModel
from persona_sync_pylib.types.chat_agents import QueueRequest


class PromptHTTPRequest(BaseModel):
    prompt: str
    poll: bool = False


class PromptRabbitRequest(QueueRequest):
    pass
