from typing import Union, Optional

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
