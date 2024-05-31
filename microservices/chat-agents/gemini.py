import google.generativeai as genai
from typing import Optional

from constants import GEMINI_MODEL
from singleton import singleton
from logger import Logger, LogLevel


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
