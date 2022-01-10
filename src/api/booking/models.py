from django.db import models
from booking.domain import model


class Seat(models.Model):
    row = models.CharField(max_length=255, null=False)
    place = models.PositiveBigIntegerField(null=False)

    class Meta:
        unique_together = ("row", "place")
        indexes = [
            models.Index(fields=["row", "place"]),
        ]

    def to_domain(self) -> model.Seat:
        return model.Seat(self.row, self.place)


class Movie(models.Model):
    movie_id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=1023, null=False)

    def to_domain(self) -> model.Movie:
        return model.Movie(self.movie_id, self.title)


class Theatre(models.Model):
    theatre_id = models.UUIDField(primary_key=True)
    seats = models.ManyToManyField(Seat)

    def to_domain(self) -> model.Theatre:
        seats = (seat.to_domain() for seat in self.seats)
        return model.Theatre(self.theatre_id, seats)


class Screening(models.Model):
    screening_id = models.UUIDField(primary_key=True)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def to_domain(self) -> model.Screening:
        reservations = (r.to_domain() for r in self.reservations)
        return model.Screening(
            reservations, self.theatre, self.movie.id, self.screening_id
        )


class Reservation(models.Model):
    reservation_number = models.UUIDField(primary_key=True)
    seats = models.ManyToManyField(Seat)
    screening = models.ForeignKey(
        Screening, related_name="reservations", on_delete=models.CASCADE
    )
    customer_id = models.UUIDField(null=False)

    def to_domain(self) -> model.Reservation:
        seats = (seat.to_domain() for seat in self.seats)
        return model.Reservation(seats, self.customer_id, self.reservation_number)