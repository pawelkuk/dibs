import string
from rest_framework import serializers
import uuid


def uuid_format(data):
    try:
        uuid.UUID(data)
    except Exception:
        raise serializers.ValidationError("Badly formed hexadecimal UUID string")


def validate_seats_data(data):
    if not isinstance(data, list):
        raise serializers.ValidationError("Please provide a list")
    if len(data) != 2:
        raise serializers.ValidationError("List has to have exactly 2 elemnts")
    if type(data[0]) != str or type(data[1]) != int:
        raise serializers.ValidationError(
            (
                "First element (seat row) has to be a string and "
                "second element (seat column) has to be an integer"
            )
        )
    if data[0] not in {*string.ascii_lowercase}:
        raise serializers.ValidationError("Row has to be a single lowercase letter")
    if data[1] < 1:
        raise serializers.ValidationError("Column number has to be a positive integer")


class DibsSerializer(serializers.Serializer):
    amount = serializers.DecimalField(decimal_places=2, max_digits=10, min_value=0)
    currency = serializers.ChoiceField(choices=("PLN", "GBP", "USD"))
    customer_id = serializers.CharField(validators=[uuid_format])
    screening_id = serializers.CharField(validators=[uuid_format])
    reservation_number = serializers.CharField(validators=[uuid_format])
    details = serializers.JSONField()
    seats_data = serializers.ListField(
        child=serializers.ListField(
            max_length=2, min_length=2, validators=[validate_seats_data]
        ),
        allow_empty=False,
    )
