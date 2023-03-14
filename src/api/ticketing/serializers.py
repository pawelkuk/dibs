from rest_framework import serializers
from ticketing import models


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = [
            "ticket_id",
            "reservation_id",
            "status",
            "ticket_url",
        ]
