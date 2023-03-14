from rest_framework import serializers
from paying import models


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment
        fields = [
            "payment_id",
            "user_id",
            "status",
        ]