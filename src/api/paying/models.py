from django.db import models


class Payment(models.Model):
    CURRENCIES = [("GBP", "GBP"), ("USD", "USD"), ("PLN", "PLN")]
    payment_id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField(null=False)
    status = models.CharField(max_length=255, null=False)
    amount = models.DecimalField(null=False, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, null=False)
