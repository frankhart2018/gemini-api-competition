from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from bson import ObjectId
import time
from persona_sync_pylib.queue import publish_message

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
    interaction_id = str(ObjectId())
    rabbit_request = PromptRabbitRequest(
        input=prompt_http_request.prompt, state="PROMPT", interaction_id=interaction_id
    )
    publish_status = publish_message(message=rabbit_request, queue_name=QUEUE_NAME)

    result_dict = {"status": publish_status, "interaction_id": interaction_id}
    if prompt_http_request.poll:
        while True:
            result = PromptInputDao().get_prompt_input(prompt_id=interaction_id)
            if result is not None:
                result_dict["output"] = result.previous_response
                break

            time.sleep(2)

    return result_dict


@router.get("/prompt/{interaction_id}", tags=["gemini-agents"])
async def get_prompt(interaction_id: str):
    result = PromptInputDao().get_prompt_input(prompt_id=interaction_id)
    if result is None:
        return HTTPException(
            status_code=404, detail="Interaction ID not found in the database"
        )

    return {
        "output": result.previous_response,
    }


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
    publish_status = publish_message(message=rabbit_request, queue_name=QUEUE_NAME)

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
        publish_status = publish_message(message=rabbit_request, queue_name=QUEUE_NAME)

        return {"status": publish_status}
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Bad request, fix this interaction"
        )
