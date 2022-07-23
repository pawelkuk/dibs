from django.db import models
from paying.domain import model


class Payment(models.Model):
    CURRENCIES = [
        (k, k) for k, _ in model.Currency.__dict__.items() if not k.startswith("_")
    ]
    payment_id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(null=False)
    status = models.CharField(max_length=255, null=False)
    amount = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=False)

    def to_domain(self) -> model.Payment:
        return model.Payment(
            payment_id=self.payment_id,
            user_id=self.user_id,
            status=model.PaymentStatus[self.status],
            amount=self.amount,
            currency=model.Currency[self.currency],
        )

    @staticmethod
    def update_from_domain(payment: model.Payment):
        p, _ = Payment.objects.get_or_create(payment_id=payment.payment_id)
        p.user_id = payment.user_id
        p.status = payment.status.value
        p.amount = payment.amount
        p.currency = payment.currency.value
        p.save()
        return p
