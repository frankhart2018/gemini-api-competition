from typing import Union, Optional
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.chat_agents import QueueRequest, StateMachineQueueRequest

from ..utils.gemini import GeminiAPIDao
from ..store.prompt_input_dao import PromptInputDao
from .handler import Handler


@singleton
class PromptHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model

    def execute(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> Optional[str]:
        model_response = self.__model.prompt(message=prompt_request.input)

        print(f"PROMPT: {model_response}")

        result = prompt_request.model_copy(deep=True)
        result.previous_response = model_response
        PromptInputDao().upsert(prompt_input=result, prompt_id=result.interaction_id)

        return None

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ):
        # No transition function from PROMPT state
        pass
