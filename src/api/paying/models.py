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
