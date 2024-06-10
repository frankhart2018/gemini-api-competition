from persona_sync_pylib.utils.prompt_inputs import PromptState

from .state_handlers import (
    Handler,
    PromptHandler,
    CommenceHandlder,
    CommunicationHandler,
)
from .state_handlers import AskGeminiHandler, AskUserHandler, TerminalHandler
from .gemini import GeminiAPIDao


def prompt_handler_factory(state: PromptState, model: GeminiAPIDao) -> Handler:
    handler = {
        "PROMPT": PromptHandler,
        "COMMENCE": CommenceHandlder,
        "COMMUNICATE": CommunicationHandler,
        "ASK_GEMINI": AskGeminiHandler,
        "ASK_USER": AskUserHandler,
        "TERMINAL": TerminalHandler,
    }

    return handler[state](model=model)
