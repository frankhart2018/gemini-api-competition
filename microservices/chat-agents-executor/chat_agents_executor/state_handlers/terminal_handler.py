from typing import Union, Optional
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.chat_agents import (
    QueueRequest,
    StateMachineQueueRequest,
)
from persona_sync_pylib.utils.logger import Logger, LogLevel

from ..store.prompt_input_dao import PromptInputDao
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
