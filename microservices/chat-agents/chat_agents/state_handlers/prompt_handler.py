from typing import Union

from ..singleton import singleton
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest
from .handler import Handler


@singleton
class PromptHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model

    def execute(self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]):
        model_response = self.__model.prompt(message=prompt_request.input)
        print(f"You: {prompt_request.input}")
        print(f"Gemini: {model_response}")  # Replace this with mongo insert call

    def transition(self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]):
        # No transition function from PROMPT state
        pass
