from typing import Union, Optional

from ..singleton import singleton
from ..gemini import GeminiAPIDao
from ..prompt_inputs import QueueRequest, StateMachineQueueRequest, PromptState
from ..logger import Logger, LogLevel
from ..queue.publisher import publish_message
from .handler import Handler


# TODO: Implement this
@singleton
class AskGeminiHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model
        self.__prompt_template = """
This is what you know about a person: <KNOWLEDGE>{user_summary}</KNOWLEDGE>. 
Given this, answer the following question in <ASK>[question]<ASK> tags: {questions}

For questions whose answer is not in <KNOWLEDGE> return the same questions in <ASK>[question]</ASK> format. 
If the answer is in <KNOWLEDGE> return only the answer in <ANS>[answer]</ANS> format. Do not make up facts.
If you add <ANS>[answer]</ANS> do not copy the <ASK>[question]</ASK>.
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
                "COMMENCE HANDLER: QueueRequest is not supported, must be StateMachineQueueRequest",
            )
            return None

        prompt_request_dict = prompt_request.model_dump()
        target = prompt_request.target
        prompt = self.__prompt_template.format(
            user_summary=prompt_request_dict[f"{target}_summary"],
            questions=prompt_request.questions,
        )
        model_response = self.__model.prompt(message=prompt)
        print(f"ASK_GEMINI: {model_response}")
        return model_response

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: Optional[str] = None,
    ) -> None:
        questions = super()._extract_text_between_tags(model_output, "ASK")

        if len(questions) > 0:
            transition_request = prompt_request.model_copy(deep=True)
            transition_request.questions = questions
            transition_request.state = PromptState.ASK_USER
            publish_message(message=transition_request)
        else:
            pass  # Transition to COMM
