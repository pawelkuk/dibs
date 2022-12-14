from random import random
from uuid import UUID, uuid4
from enum import Enum


class PaymentError(Exception):
    pass


class Currency(Enum):
    USD = "USD"
    PLN = "PLN"
    GBP = "GBP"


class PaymentStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class Payment:
    def __init__(
        self,
        user_id: UUID,
        amount: str,
        currency: Currency,
        status: PaymentStatus = None,
        payment_id: UUID = None,
    ):
        self.payment_id = payment_id
        self.user_id = user_id
        self.status = status
        self.amount = amount
        self.currency = currency

    def pay(self, payment_success_rate: float) -> UUID:
        if self.status == PaymentStatus.SUCCESS and self.payment_id:
            return self.payment_id

        if not self.user_id or not self.amount or not self.currency:
            raise PaymentError("Insufficient information to process payment")

        self.payment_id = self.request_to_payment_provider(payment_success_rate)
        return self.payment_id

    def request_to_payment_provider(self, payment_success_rate: float):
        if random() < payment_success_rate:
            # Happy path
            self.status = PaymentStatus.SUCCESS
            return uuid4()
        else:
            self.status = PaymentStatus.FAILED
            self.payment_id = uuid4()
            raise PaymentError("Problem with payment provider. Try again!")

    def refund(self) -> UUID:
        if not self.payment_id or self.status != PaymentStatus.SUCCESS:
            raise PaymentError("You can't get back a money you didn't pay")

        self.request_to_payment_provider_refund()
        self.status = PaymentStatus.CANCELED

    def request_to_payment_provider_refund(self):
        # This would be a request to a payment provider
        # To simplify this case we assume this request always succeeds
        ...
