from typing import Union, Optional
from persona_sync_pylib.queue import publish_chat_agents_message
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.chat_agents import (
    QueueRequest,
    StateMachineQueueRequest,
    PromptState,
    QAndA,
)
from persona_sync_pylib.utils.logger import Logger, LogLevel

from ..utils.environment import MAX_INTERACTIONS, QUEUE_NAME
from ..utils.gemini import GeminiAPIDao
from .handler import Handler


@singleton
class CommunicationHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model
        self.__prompt_template = """
You are going to impersonate a person, whose summary is: <YOUR-SUMMARY>{your_summary}</YOUR-SUMMARY>.
This is the information about the person you are going to talk to: <THEIR-SUMMARY>{their_summary}</THEIR-SUMMARY>.
They have sent you this message: <THEIR-MESSAGE>{their_message}</THEIR-MESSAGE>. Their message might contain
questions that they have asked you. Their question to you and your answers to those questions can be found here: 
{your_q_and_a_s}, each question is wrapped in <ASK></ASK> tags and is immediately followed by the answer in <ANS></ANS> tags. 
Send them a response, in response you can answer their questions and ask questions to them. Paste the answers
as is, do not add extra to them and remove the <ANS></ANS> tags before sending them. 
All questions that you ask them should be wrapped in <ASK> as: <ASK>[question]</ASK> where [question] is your
question to them. Do not ask any questions that is already in their summary. 
Do not make any facts about yourself or them, if it is not in <YOUR-SUMMARY> or <THEIR-SUMMARY> you should not
generate that.
"""

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

        if self.__can_transition_to_terminal(prompt_request):
            return "TO TERMINAL"

        target_user = prompt_request.target
        non_target_user = "u1" if target_user == "u2" else "u2"

        prompt_request_dict = prompt_request.model_dump()
        q_and_a_s = "\n".join(
            [
                f"{q_and_a.question}\n{q_and_a.answer}"
                for q_and_a in prompt_request.q_and_a_s
            ]
        )

        prompt = self.__prompt_template.format(
            your_summary=prompt_request_dict[f"{target_user}_summary"],
            their_summary=prompt_request_dict[f"{non_target_user}_summary"],
            their_message=prompt_request.previous_response,
            your_q_and_a_s=q_and_a_s,
        )
        model_response = self.__model.prompt(message=prompt)
        print(f"COMMUNICATE: {model_response}")
        return model_response

    def __can_transition_to_terminal(
        self, prompt_request: StateMachineQueueRequest
    ) -> bool:
        if prompt_request.interaction_length == MAX_INTERACTIONS:
            return True

        return False

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ) -> None:
        if model_output == "TO TERMINAL":
            transition_request = prompt_request.model_copy(deep=True)
            transition_request.state = PromptState.TERMINAL
            publish_chat_agents_message(
                message=transition_request, queue_name=QUEUE_NAME
            )
            return

        questions = super()._extract_text_between_tags(model_output, "ASK")
        transition_request = prompt_request.model_copy(deep=True)
        transition_request.interaction_length += 1

        if len(questions) > 0:
            transition_request.target = "u1" if prompt_request.target == "u2" else "u2"
            transition_request.q_and_a_s = [
                QAndA(question=question) for question in questions
            ]
            transition_request.previous_response = model_output
            transition_request.state = PromptState.ASK_GEMINI
            publish_chat_agents_message(
                message=transition_request, queue_name=QUEUE_NAME
            )
        else:
            transition_request.target = "u1" if prompt_request.target == "u2" else "u2"
            transition_request.previous_response = model_output
            transition_request.state = PromptState.COMMUNICATE
            publish_chat_agents_message(
                message=transition_request, queue_name=QUEUE_NAME
            )
