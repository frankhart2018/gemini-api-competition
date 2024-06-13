from typing import Union, Optional, List
from dataclasses import dataclass
from persona_sync_pylib.queue import publish_chat_agents_message
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.types.chat_agents import (
    QueueRequest,
    StateMachineQueueRequest,
    PromptState,
    UserQuestion,
    UserQuestionState,
    QAndA,
)
from persona_sync_pylib.utils.logger import Logger, LogLevel

from ..store.prompt_input_dao import PromptInputDao
from ..store.user_questions_dao import UserQuestionsDao
from ..utils.gemini import GeminiAPIDao
from ..utils.environment import QUEUE_NAME
from .handler import Handler


@dataclass
class QuestionAndEmbedding:
    question: QAndA
    embedding: List[float]


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

        prompt_request_dict = prompt_request.model_dump()
        q_and_a_s = prompt_request.q_and_a_s
        answered_q_and_a_s = []
        unanswered_q_and_a_s: List[QuestionAndEmbedding] = []

        all_user_questions = UserQuestionsDao().find_questions_for_user(
            user_id=prompt_request_dict[f"{prompt_request.target}_uid"]
        )

        accept_score = 0
        reject_score = 0
        num_accepted = 0
        num_rejected = 0

        for q_and_a in q_and_a_s:
            if q_and_a.answer:
                answered_q_and_a_s.append(q_and_a)
            else:
                embedding = GeminiAPIDao().get_embeddings(message=q_and_a.question)
                unanswered_q_and_a_s.append(
                    QuestionAndEmbedding(question=q_and_a, embedding=embedding)
                )

        filtered_unanswered_q_and_a_s = []
        for qa_and_embedding in unanswered_q_and_a_s:
            q_and_a = qa_and_embedding.question
            embedding = qa_and_embedding.embedding

            for user_question in all_user_questions:
                if user_question.state == UserQuestionState.ANSWERED:
                    accept_score += GeminiAPIDao().get_similarity_score(
                        embedding_1=embedding,
                        embedding_2=user_question.question_embedding,
                    )
                    num_accepted += 1
                elif user_question.state == UserQuestionState.REJECTED:
                    reject_score += GeminiAPIDao().get_similarity_score(
                        embedding_1=embedding,
                        embedding_2=user_question.question_embedding,
                    )
                    num_rejected += 1

            avg_accept_score = accept_score / num_accepted if num_accepted > 0 else 0
            avg_reject_score = reject_score / num_rejected if num_rejected > 0 else 0

            if avg_accept_score >= avg_reject_score:
                UserQuestionsDao().insert(
                    user_question=UserQuestion(
                        user_id=prompt_request_dict[f"{prompt_request.target}_uid"],
                        question=q_and_a.question,
                        question_embedding=embedding,
                        question_id=q_and_a.obj_id,
                        interaction_id=prompt_request.interaction_id,
                        state=UserQuestionState.PENDING,
                        answer="",
                    )
                )
                filtered_unanswered_q_and_a_s.append(q_and_a)

        if len(filtered_unanswered_q_and_a_s) == 0:
            print(f"ASK_USER: No worthy questions to ask!")
            return None
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
        pass
