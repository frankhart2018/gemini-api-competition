from typing import Union, Optional
import re

from ..prompt_inputs import QueueRequest, StateMachineQueueRequest


class Handler:
    def execute(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> Optional[str]:
        raise NotImplementedError(
            "Do not use the base handler class directly. Use a subclass instead."
        )

    def transition(
        self,
        prompt_request: Union[QueueRequest, StateMachineQueueRequest],
        model_output: Optional[str] = None,
    ) -> None:
        raise NotImplementedError(
            "Do not use the base handler class directly. Use a subclass instead."
        )

    def _extract_text_between_tags(self, text, tag):
        if not text:
            return ""

        pattern = f"<{tag}>(.*?)</{tag}>"
        matches = re.findall(pattern, text, re.DOTALL)
        matches = [f"<{tag}>{match}</{tag}>" for match in matches]
        return "\n".join(matches)

    def _extract_text_outside_tags(self, text, tag):
        if not text:
            return ""

        pattern = f"<{tag}>.*?</{tag}>"
        segments = re.split(pattern, text, flags=re.DOTALL)
        result = "".join([re.sub(r"\s+", " ", segment.strip()) for segment in segments])
        return result
