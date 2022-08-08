from rest_framework import serializers
from booking import models


class ScreeningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Screening
        fields = [
            "screening_id",
            "theatre",
            "movie",
            "reservations",
        ]
