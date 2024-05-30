import google.generativeai as genai

from constants import GEMINI_MODEL
from singleton import singleton


@singleton
class GeminiAPIDao:
    def __init__(self, api_key: str) -> None:
        genai.configure(api_key=api_key)
        self.__model = genai.GenerativeModel(model_name=GEMINI_MODEL)

    def prompt(self, message: str) -> str:
        message_formatted = {"role": "user", "parts": [message]}

        try:
            response = self.__model.generate_content(message_formatted)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error while prompting Gemini: {e}")
