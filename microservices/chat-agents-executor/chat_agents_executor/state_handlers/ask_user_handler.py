from typing import Union, Optional

from ..singleton import singleton
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest
from ..logger import Logger, LogLevel
from ..mongo_ops import PromptInputDao
from ..prompt_inputs import PromptState
from ..queue.publisher import publish_message
from .handler import Handler


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

        q_and_a_s = prompt_request.q_and_a_s
        answered_q_and_a_s = []
        unanswered_q_and_a_s = []

        for q_and_a in q_and_a_s:
            if q_and_a.answer:
                answered_q_and_a_s.append(q_and_a)
            else:
                unanswered_q_and_a_s.append(q_and_a)

        if len(unanswered_q_and_a_s) == 0:
            print(f"ASK_USER: No questions to ask!")
            return "To COMM"
        else:
            PromptInputDao().upsert(
                prompt_input=prompt_request, prompt_id=prompt_request.interaction_id
            )
            print(f"ASK_USER: Posted to user!")
            return None

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ) -> None:
        transition_request = prompt_request.model_copy(deep=True)
        transition_request.state = PromptState.COMMUNICATE
        publish_message(message=transition_request)
