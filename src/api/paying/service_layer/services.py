from paying.service_layer import unit_of_work
from uuid import UUID
from paying.domain import model


def pay(
    user_id: UUID,
    amount: str,
    currency: model.Currency,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        payment = model.Payment(amount=amount, currency=currency, user_id=user_id)
        payment_id = payment.pay()
        uow.payments.add(payment=payment)
        uow.commit()
    return payment_id
