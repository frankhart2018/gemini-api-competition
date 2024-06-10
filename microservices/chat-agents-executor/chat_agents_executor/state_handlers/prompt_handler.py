from typing import Union, Optional
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.prompt_inputs import QueueRequest, StateMachineQueueRequest

from ..gemini import GeminiAPIDao
from .handler import Handler


@singleton
class PromptHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model

    def execute(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> Optional[str]:
        model_response = self.__model.prompt(message=prompt_request.input)
        print(f"You: {prompt_request.input}")
        print(f"Gemini: {model_response}")  # Replace this with mongo insert call

        return None

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ):
        # No transition function from PROMPT state
        pass
