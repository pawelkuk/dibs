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


class Payment:
    def __init__(
        self,
        payment_id: UUID,
        user_id: UUID,
        status: PaymentStatus,
        amount: str,
        currency: Currency,
    ):
        self.payment_id = payment_id
        self.user_id = user_id
        self.status = status.value
        self.amount = amount
        self.currency = currency.value

    def pay(self, user_id: UUID, amount: str, currency: Currency) -> UUID:
        if self.status == PaymentStatus.SUCCESS and self.payment_id:
            return self.payment_id

        if not user_id or not amount or not currency:
            raise PaymentError("Insufficient informatation to process payment")
        self.user_id = user_id
        self.amount = amount
        self.currency = currency

        self.payment_id = self.request_to_payment_provider()
        return self.payment_id

    def request_to_payment_provider(self):
        if random() < 0.90:
            # Happy path
            self.status = PaymentStatus.SUCCESS
            return uuid4()
        else:
            self.status = PaymentStatus.FAILED
            self.payment_id = uuid4()
            raise PaymentError("Problem with payment provider. Try again!")
