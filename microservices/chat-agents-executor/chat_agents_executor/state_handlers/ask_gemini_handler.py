from typing import Union, Optional
from persona_sync_pylib.queue import publish_message
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.prompt_inputs import QueueRequest, StateMachineQueueRequest, PromptState, QAndA
from persona_sync_pylib.utils.logger import Logger, LogLevel

from ..gemini import GeminiAPIDao
from .handler import Handler


@singleton
class AskGeminiHandler(Handler):
    def __init__(self, model: GeminiAPIDao) -> None:
        self.__model = model
        self.__prompt_template = """
This is what you know about a person: <KNOWLEDGE>{user_summary}</KNOWLEDGE>. 
Given this, answer the following questions in <ASK>[question]<ASK> tags: {questions}

For questions whose answer is not in <KNOWLEDGE> return the same questions in <ASK>[question]</ASK> format. 
If the answer is in <KNOWLEDGE> return only the answer in <ANS>[answer]</ANS> format. Do not make up facts.
If you do not have the answer then return an empty <ANS></ANS> tag. All questions should be copied, and
the order should be preserved. Each answer should follow the corresponding question. 
Do not make up additional questions. The number of <ASK> and <ANS> tags should be the same.
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

        questions_list = [q_and_a.question for q_and_a in prompt_request.q_and_a_s]

        prompt = self.__prompt_template.format(
            user_summary=prompt_request_dict[f"{target}_summary"],
            questions="\n".join(questions_list),
        )
        model_response = self.__model.prompt(message=prompt)
        print(f"ASK_GEMINI: {model_response}")
        return model_response

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: str,
    ) -> None:
        questions = super()._extract_text_between_tags(model_output, "ASK")
        answers = super()._extract_text_between_tags(model_output, "ANS")

        answered_q_and_a_s = []
        unanswered_q_and_a_s = []
        for question, answer in zip(questions, answers):
            if answer.strip() == "<ANS></ANS>":
                unanswered_q_and_a_s.append(QAndA(question=question))
            else:
                answered_q_and_a_s.append(QAndA(question=question, answer=answer))

        transition_request = prompt_request.model_copy(deep=True)

        if len(unanswered_q_and_a_s) > 0:
            questions = answered_q_and_a_s + unanswered_q_and_a_s
            transition_request.q_and_a_s = questions

            transition_request.state = PromptState.ASK_USER
            publish_message(message=transition_request)
        else:
            transition_request.q_and_a_s = answered_q_and_a_s
            transition_request.state = PromptState.COMMUNICATE
            publish_message(message=transition_request)
