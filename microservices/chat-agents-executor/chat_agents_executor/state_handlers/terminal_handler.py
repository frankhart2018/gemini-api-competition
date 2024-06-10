from typing import Union, Optional
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.prompt_inputs import QueueRequest, StateMachineQueueRequest, PromptState, QAndA
from persona_sync_pylib.utils.logger import Logger, LogLevel
from persona_sync_pylib.utils.mongo_ops import PromptInputDao

from ..gemini import GeminiAPIDao
from .handler import Handler


@singleton
class TerminalHandler(Handler):
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
                "COMMUNICATE HANDLER: QueueRequest is not supported, must be StateMachineQueueRequest",
            )
            return None

        PromptInputDao().upsert(
            prompt_input=prompt_request, prompt_id=prompt_request.interaction_id
        )
        print("TERMINAL: TERMINATING")
        return None

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ) -> None:
        pass
