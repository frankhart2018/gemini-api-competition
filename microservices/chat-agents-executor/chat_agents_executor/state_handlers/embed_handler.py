from typing import Union, Optional
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.chat_agents import (
    QueueRequest,
    StateMachineQueueRequest,
    ValEmbeddings,
)

from ..utils.gemini import GeminiAPIDao
from ..store.val_embeddings_dao import ValEmbeddingsDao
from .handler import Handler


@singleton
class EmbedHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model

    def execute(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> Optional[str]:
        model_response = self.__model.get_embeddings(message=prompt_request.input)

        print(f"EMBED: {len(model_response)}")

        val_embedding = ValEmbeddings(
            tracking_id=prompt_request.interaction_id,
            value=prompt_request.input,
            embeddings=model_response,
        )
        ValEmbeddingsDao().upsert(
            val_embedding=val_embedding, tracking_id=prompt_request.interaction_id
        )

        return None

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ):
        # No transition function from EMBED state
        pass
