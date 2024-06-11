from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from persona_sync_pylib.queue import publish_chat_agents_message

from app.store.prompt_input_dao import PromptInputDao
from app.model.prompt_request import PromptHTTPRequest, PromptRabbitRequest
from app.model.initiate_request import (
    InitiateChatHTTPRequest,
    InitiateChatRabbitRequest,
)
from app.model.revert_request import RevertChatHTTPRequest, RevertChatRabbitRequest
from app.utils.environment import QUEUE_NAME


router = APIRouter()


@router.post("/prompt", tags=["gemini-agents"])
async def prompt(prompt_http_request: PromptHTTPRequest):
    rabbit_request = PromptRabbitRequest(
        input=prompt_http_request.prompt, state="PROMPT"
    )
    publish_status = publish_chat_agents_message(
        message=rabbit_request, queue_name=QUEUE_NAME
    )

    return {"status": publish_status}


@router.post("/chat/initiate", tags=["gemini-agents"])
async def chat(initiate_chat_http_request: InitiateChatHTTPRequest):
    rabbit_request = InitiateChatRabbitRequest(
        input="",
        state="COMMENCE",
        u1_uid=initiate_chat_http_request.u1_uid,
        u2_uid=initiate_chat_http_request.u2_uid,
        u1_summary=initiate_chat_http_request.u1_summary,
        u2_summary=initiate_chat_http_request.u2_summary,
        target="u1",
    )
    publish_status = publish_chat_agents_message(
        message=rabbit_request, queue_name=QUEUE_NAME
    )

    return {"status": publish_status}


@router.post("/chat/revert/{interaction_id}", tags=["gemini-agents"])
async def chat_revert(
    interaction_id: str, revert_chat_http_request: RevertChatHTTPRequest
):
    q_and_a_s = [q_and_a.model_dump() for q_and_a in revert_chat_http_request.q_and_a_s]
    result = PromptInputDao().update_questions_answers(
        interaction_id=interaction_id, q_and_a_s=q_and_a_s
    )

    if result is None:
        return HTTPException(
            status_code=404, detail="Interaction ID not found in the database"
        )

    try:
        rabbit_request = RevertChatRabbitRequest(**result)
        publish_status = publish_chat_agents_message(
            message=rabbit_request, queue_name=QUEUE_NAME
        )

        return {"status": publish_status}
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Bad request, fix this interaction"
        )
