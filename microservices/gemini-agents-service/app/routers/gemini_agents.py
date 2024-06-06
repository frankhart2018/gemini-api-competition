from fastapi import APIRouter

from app.model.prompt_request import PromptHTTPRequest, PromptRabbitRequest
from app.utils.queue import publish_message


router = APIRouter()


@router.post("/prompt", tags=["gemini-agents"])
async def prompt(prompt_http_request: PromptHTTPRequest):
    rabbit_request = PromptRabbitRequest(prompt=prompt_http_request.prompt)
    publish_status = publish_message(message=rabbit_request.model_dump_json())

    return {"status": publish_status}
