from paying.service_layer import unit_of_work
from uuid import UUID
from paying.domain import model


def pay(
    user_id: UUID,
    amount: str,
    currency: model.Currency,
    uow: unit_of_work.AbstractUnitOfWork,
    payment_success_rate: float,
):
    with uow:
        payment = model.Payment(amount=amount, currency=currency, user_id=user_id)
        payment_id = payment.pay(payment_success_rate)
        uow.repo.add(payment)
        uow.commit()
    return payment_id


def refund(
    payment_id: UUID,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        payment: model.Payment = uow.repo.get(
            model.Payment, domain_model_instance_id=payment_id
        )
        payment_id = payment.refund()
        uow.commit()
    return payment_id
