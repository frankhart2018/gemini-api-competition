from typing import Union, Optional

from ..singleton import singleton
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest
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
