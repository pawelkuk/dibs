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
    endpoint_kwargs = None
    compensation_endpoint = None
    compensation_kwargs = None

    def __init__(self, **endpoint_kwargs):
        self.endpoint_kwargs = endpoint_kwargs

    def make_request(self, endpoint: str, expected_input: dict[str, Any]):
        print(f"http://app/{endpoint}")
        res = requests.post(f"http://app/{endpoint}", json=expected_input)
        success = res.status_code < 400
        if success:
            self.compensation_kwargs = res.json()
        return self.compensation_kwargs, success

    def make(self, expected_input: dict[str, Any]):
        return self.make_request(
            self.endpoint, {**self.endpoint_kwargs, **expected_input}
        )

    def compensate(self, expected_input: dict[str, Any]):
        return self.make_request(self.compensation_endpoint, self.compensation_kwargs)[
            0
        ]


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
    def __init__(self, steps: Iterable[SagaStep]) -> None:
        self.steps = steps

    def do(self) -> bool:
        failed_step = None

        next_input = {}
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
    reservation_kwargs = {
        "customer_id": init_input["customer_id"],
        "screening_id": init_input["screening_id"],
        "reservation_number": init_input["reservation_number"],
        "seats_data": init_input["seats_data"],
    }
    payment_kwargs = {
        "user_id": init_input["customer_id"],
        "reservation_number": init_input["reservation_number"],
        "amount": str(init_input["amount"]),
        "currency": init_input["currency"].value,
    }
    ticket_kwargs = {
        "reservation_id": init_input["reservation_number"],
        "details": init_input["details"],
    }

    saga = Saga(
        steps=[
            ReservationStep(**reservation_kwargs),
            PaymentStep(**payment_kwargs),
            TicketingStep(**ticket_kwargs),
        ]
    )
    if success := saga.do():
        print("success")
    else:
        print("failed")
