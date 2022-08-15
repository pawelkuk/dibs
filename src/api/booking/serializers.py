from rest_framework import serializers
from booking import models


class ReservationSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()

    class Meta:
        model = models.Reservation
        fields = [
            "reservation_number",
            "seats",
            "customer_id",
        ]

    def get_seats(self, obj):
        return ["".join(x) for x in obj.seats]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = ["title"]


class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Theatre
        fields = ["theatre_id"]


class ScreeningSerializer(serializers.ModelSerializer):
    theatre = TheatreSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Screening
        fields = [
            "screening_id",
            "theatre",
            "movie",
            "reservations",
        ]
