from typing import Union

from ..prompt_inputs import QueueRequest, StateMachineQueueRequest


class Handler:
    def execute(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> None:
        raise NotImplementedError(
            "Do not use the base handler class directly. Use a subclass instead."
        )

    def transition(
        self, prompt_request: Union[QueueRequest, StateMachineQueueRequest]
    ) -> None:
        raise NotImplementedError(
            "Do not use the base handler class directly. Use a subclass instead."
        )
