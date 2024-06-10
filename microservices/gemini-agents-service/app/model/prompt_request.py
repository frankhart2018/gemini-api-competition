from pydantic import BaseModel
from persona_sync_pylib.utils.prompt_inputs import QueueRequest


class PromptHTTPRequest(BaseModel):
    prompt: str


class PromptRabbitRequest(QueueRequest):
    pass
