import google.generativeai as genai
from typing import Optional, List
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.logger import Logger, LogLevel

from .environment import GEMINI_MODEL, EMBED_MODEL


@singleton
class GeminiAPIDao:
    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.__model = genai.GenerativeModel(model_name=GEMINI_MODEL)

    def prompt(self, message: str) -> Optional[str]:
        message_formatted = {"role": "user", "parts": [message]}

        try:
            response = self.__model.generate_content(message_formatted)
            return response.text
        except Exception as e:
            Logger().log(LogLevel.ERROR, f"Failed to generate content: {e}")
            return None

    def get_embeddings(self, message: str) -> List[float]:
        try:
            response = genai.embed_content(
                model=EMBED_MODEL,
                content=message,
                task_type="SEMANTIC_SIMILARITY",
            )
            return response["embedding"]
        except Exception as e:
            Logger().log(LogLevel.ERROR, f"Failed to generate embeddings: {e}")
            return []
