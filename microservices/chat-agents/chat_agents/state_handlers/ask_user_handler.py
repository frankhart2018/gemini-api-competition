from typing import Union, Optional

from ..singleton import singleton
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest
from ..logger import Logger, LogLevel
from ..mongo_ops import PromptInputDao
from .handler import Handler


# TODO: Implement this
@singleton
class AskUserHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model

    def execute(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> Optional[str]:
        if (
            isinstance(prompt_request, QueueRequest)
            and type(prompt_request) != StateMachineQueueRequest
        ):
            Logger().log(
                LogLevel.ERROR,
                "COMMENCE HANDLER: QueueRequest is not supported, must be StateMachineQueueRequest",
            )
            return None

        questions = super()._extract_text_between_tags(prompt_request.questions, "ASK")

        if len(questions) == 0:
            return None

        PromptInputDao().upsert(
            prompt_input=prompt_request, prompt_id=prompt_request.interaction_id
        )
        print(f"ASK_USER: Posted to user!")
        return None

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: Optional[str] = None,
    ) -> None:
        questions = super()._extract_text_between_tags(model_output, "ASK")

        if len(questions) == 0:
            pass  # Transition to COMM
