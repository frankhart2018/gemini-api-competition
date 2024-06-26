from persona_sync_pylib.types.chat_agents import PromptState

from ..state_handlers import (
    Handler,
    PromptHandler,
    CommenceHandlder,
    CommunicationHandler,
)
from ..state_handlers import (
    AskGeminiHandler,
    AskUserHandler,
    TerminalHandler,
    EmbedHandler,
)
from .gemini import GeminiAPIDao


def prompt_handler_factory(state: PromptState, model: GeminiAPIDao) -> Handler:
    handler = {
        "PROMPT": PromptHandler,
        "COMMENCE": CommenceHandlder,
        "COMMUNICATE": CommunicationHandler,
        "ASK_GEMINI": AskGeminiHandler,
        "ASK_USER": AskUserHandler,
        "TERMINAL": TerminalHandler,
        "EMBED": EmbedHandler,
    }

    return handler[state](model=model)
