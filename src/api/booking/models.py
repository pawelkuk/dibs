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
        m, _ = Movie.objects.get_or_create(movie_id=movie.movie_id, title=movie.title)
        return m


class Theatre(models.Model):
    theatre_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seats = ArrayField(
        ArrayField(models.CharField(max_length=3, null=False), size=2),
    )

    def to_domain(self) -> model.Theatre:
        import ipdb

        ipdb.set_trace()
        seats = (model.Seat(row=seat[0], place=seat[1]) for seat in self.seats)
        return model.Theatre(self.theatre_id, seats)

    @staticmethod
    def from_domain(theatre: model.Theatre):
        t, _ = Theatre.objects.get_or_create(
            theatre_id=theatre.theatre_id,
            seats=[[s.row, s.place] for s in theatre.seats],
        )
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
            reservations, self.theatre, self.movie.movie_id, self.screening_id
        )

    @staticmethod
    def update_from_domain(screening: model.Screening):
        try:
            s = Screening.objects.get(screening_id=screening.screening_id)
        except Screening.DoesNotExist:
            s = Screening(screening_id=screening.screening_id)
            s.movie = (Movie.from_domain(screening.movie),)
            s.theatre = (Theatre.from_domain(screening.theatre),)
            s.save()
            s.reservations.set(
                Reservation.from_domain(r) for r in screening._reservations
            )


class Reservation(models.Model):
    reservation_number = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    seats = ArrayField(
        ArrayField(models.CharField(max_length=3, null=False), size=2, null=False),
    )
    screening = models.ForeignKey(
        Screening, related_name="reservations", on_delete=models.CASCADE
    )
    customer_id = models.UUIDField(null=False)

    def to_domain(self) -> model.Reservation:
        seats = (model.Seat(row=s[0], place=s[1]) for s in self.seats)
        return model.Reservation(seats, self.customer_id, self.reservation_number)

    @staticmethod
    def from_domain(reservation: model.Reservation):
        r, _ = Reservation.objects.get_or_create(
            reservation_number=reservation.reservation_number,
            seats=[[s.row, s.place] for s in reservation.seats],
            customer_id=reservation.customer_id,
        )
        return r
