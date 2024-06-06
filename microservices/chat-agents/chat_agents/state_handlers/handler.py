from typing import Union, Optional, List
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
        model_output: str,
    ) -> None:
        raise NotImplementedError(
            "Do not use the base handler class directly. Use a subclass instead."
        )

    def _extract_text_between_tags(self, text, tag) -> List[str]:
        pattern = f"<{tag}>(.*?)</{tag}>"
        matches = re.findall(pattern, text, re.DOTALL)
        matches = [f"<{tag}>{match.strip()}</{tag}>" for match in matches]
        return matches
