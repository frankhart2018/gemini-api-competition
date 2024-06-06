from pydantic import BaseModel
from typing import Optional


class PromptHTTPRequest(BaseModel):
    prompt: str


class PromptRabbitRequest(BaseModel):
    prompt: str
    state: Optional[str] = "PROMPT"
