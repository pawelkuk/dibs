from django.db import models
from booking.domain import model
from django.contrib.postgres.fields import ArrayField
import uuid


class Movie(models.Model):
    movie_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1023, null=False)

    def to_domain(self) -> model.Movie:
        return model.Movie(self.movie_id, self.title)

    @staticmethod
    def from_domain(movie: model.Movie):
        m, _ = Movie.objects.get_or_create(movie_id=movie.movie_id)
        m.title = movie.title
        m.save()
        return m


class Theatre(models.Model):
    theatre_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seats = ArrayField(
        ArrayField(models.CharField(max_length=3, null=False), size=2),
    )

    def to_domain(self) -> model.Theatre:
        seats = (
            model.Seat(
                row=seat[0],
                place=int(seat[1]),
                id=None,
                reservation_id=None,
                screening_id=None,
            )
            for seat in self.seats
        )
        return model.Theatre(self.theatre_id, seats)

    @staticmethod
    def from_domain(theatre: model.Theatre):
        t, _ = Theatre.objects.get_or_create(theatre_id=theatre.theatre_id)
        t.seats = [[s.row, s.place] for s in theatre.seats]
        t.save()
        return t


class Screening(models.Model):
    screening_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def to_domain(self) -> model.Screening:
        reservations = (r.to_domain() for r in self.reservations.all())
        return model.Screening(
            reservations,
            self.theatre.to_domain(),
            self.movie.to_domain(),
            self.screening_id,
        )

    @staticmethod
    def update_from_domain(screening: model.Screening):
        try:
            s = Screening.objects.get(screening_id=screening.screening_id)
        except Screening.DoesNotExist:
            s = Screening(screening_id=screening.screening_id)
        s.movie = Movie.from_domain(screening.movie)
        s.theatre = Theatre.from_domain(screening.theatre)
        s.save()
        s.reservations.set(Reservation.from_domain(r) for r in screening._reservations)


class Reservation(models.Model):
    reservation_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    screening = models.ForeignKey(
        Screening, related_name="reservations", on_delete=models.CASCADE, null=True
    )
    customer_id = models.UUIDField(null=False)

    def to_domain(self) -> model.Reservation:
        seats = (
            model.Seat(
                row=s.row,
                place=s.place,
                id=None,
                screening_id=None,
                reservation_id=None,
            )
            for s in self.reservation_seats.all()
        )
        return model.Reservation(seats, self.customer_id, self.reservation_number)

    @staticmethod
    def from_domain(reservation: model.Reservation):
        try:
            r = Reservation.objects.get(
                reservation_number=reservation.reservation_number,
            )
        except Reservation.DoesNotExist:
            r = Reservation(reservation_number=reservation.reservation_number)
        r.customer_id = reservation.customer_id
        r.seats = [[s.row, s.place] for s in reservation.seats]
        r.save()
        return r


class Seat(models.Model):
    place = models.IntegerField(null=False)
    row = models.CharField(max_length=3, null=False)
    reservation = models.ForeignKey(
        Reservation,
        related_name="reservation_seats",
        on_delete=models.CASCADE,
        null=False,
    )
    screening = models.ForeignKey(
        Screening, related_name="seats", on_delete=models.CASCADE, null=False
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "place", "screening_id"], name="no_seat_double_booking"
            )
        ]
