from typing import Union, Optional

from ..singleton import singleton
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest, PromptState
from ..logger import Logger, LogLevel
from ..queue.publisher import publish_message
from .handler import Handler


@singleton
class CommenceHandlder(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model
        self.__prompt_template = """You are going to impersonate a person, whose summary is: <YOUR-SUMMARY>{your_summary}</YOUR-SUMMARY>.
This is the information about the person you are going to talk to: <THEIR-SUMMARY>{their_summary}</THEIR-SUMMARY>.
Send them a message.
All questions that you ask them should be wrapped in <ASK> as: <ASK>[question]</ASK> where [question] is your
question to them. Do not ask any questions that is already in their summary. 
Do not make any facts about yourself or them, if it is not in <YOUR-SUMMARY> or <THEIR-SUMMARY> you should not
generate that."""

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

        prompt = self.__prompt_template.format(
            your_summary=prompt_request.u1_summary,
            their_summary=prompt_request.u2_summary,
        )
        model_response = self.__model.prompt(message=prompt)
        print(f"COMMENCE: {model_response}")
        return model_response

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: Optional[str] = None,
    ) -> None:
        questions = super()._extract_text_between_tags(model_output, "ASK")

        if len(questions) > 0:
            transition_request = prompt_request.model_copy(deep=True)
            transition_request.target = "u2"
            transition_request.questions = questions
            transition_request.previous_response = model_output
            transition_request.state = PromptState.ASK_GEMINI
            publish_message(message=transition_request)
        else:
            pass  # Transition to COMM
