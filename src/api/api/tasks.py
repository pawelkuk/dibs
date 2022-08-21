from typing import Any, Iterable
from celery import shared_task
import requests


class SagaStep:
    def make(self, expected_input: dict[str, Any]) -> tuple[dict[str, Any], bool]:
        raise NotImplementedError

    def compensate(self, expected_input: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class RequestStep(SagaStep):
    endpoint = None
    compensation_endpoint = None

    def make_request(self, endpoint: str, expected_input: dict[str, Any]):
        res = requests.post(f"app:5000/{endpoint}", expected_input)
        data = res.json()
        success = res.status_code != 400
        return data, success

    def make(self, expected_input: dict[str, Any]):
        return self.make_request(self.endpoint, expected_input)

    def compensate(self, expected_input: dict[str, Any]):
        return self.make_request(self.compensation_endpoint, expected_input)[0]


class ReservationStep(RequestStep):
    endpoint = "make-reservation"
    compensation_endpoint = "cancel-reservation"


class PaymentStep(RequestStep):
    endpoint = "pay"
    compensation_endpoint = "refund"


class TicketingStep(RequestStep):
    endpoint = "render-ticket"
    compensation_endpoint = None  # it's the last step so it's not needed


class Saga:
    def __init__(self, steps: Iterable[SagaStep], init_input: dict[str, Any]) -> None:
        self.steps = steps
        self.init_input = init_input

    def do(self) -> bool:
        failed_step = None

        next_input = self.init_input
        for idx, step in enumerate(self.steps):
            result, success = step.make(next_input)
            next_input = result
            if success:
                continue
            else:
                failed_step = idx
                break
        else:
            return True  # Great success

        # rollback succesful steps
        for step in reversed(self.steps[:failed_step]):
            next_input = step.compensate(next_input)

        return False  # Try again later


@shared_task
def dibs(init_input):
    saga = Saga(
        steps=[
            ReservationStep(),
            PaymentStep(),
            TicketingStep(),
        ],
        init_input=init_input,
    )
    if success := saga.do():
        print("success")
    else:
        print("failed")
