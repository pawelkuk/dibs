from typing import Iterable
from dataclasses import dataclass
from uuid import UUID, uuid4
from booking.domain import events


class SeatTaken(Exception):
    pass


class SeatsCollide(Exception):
    pass


class ReservationDoesNotExists(Exception):
    pass


class ScreeningDoesNotExists(Exception):
    pass


@dataclass
class Seat:
    id: int
    row: str
    place: int
    reservation_id: UUID
    screening_id: UUID

    def __hash__(self):
        hashed = hash(
            tuple(getattr(self, key) for key in ("row", "place", "screening_id"))
        )
        return hashed

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)


@dataclass
class Movie:
    movie_id: UUID
    title: str


class Theatre:
    def __init__(self, theatre_id: UUID, seats: Iterable[Seat]):
        self.theatre_id = theatre_id
        self._seats = {seat for seat in seats}

    @property
    def seats(self):
        return self._seats


class Reservation:
    def __init__(
        self, seats: Iterable[Seat], customer_id: UUID, reservation_number: UUID = None
    ):
        # FIXME: uuid should be generated in a factory, placing it here can probably
        # impact ease of testing, we will see
        self.reservation_number = reservation_number or uuid4()
        self.customer_id = customer_id
        self._seats = {seat for seat in seats}

    def add(self, seat: Seat):
        if seat not in self._seats:  # seat is available
            self._seats.add(seat)
        else:
            raise SeatTaken("This seat has already been chosen")

    @property
    def seats(self):
        return self._seats

    def __hash__(self) -> int:
        return hash(self.reservation_number)


class Screening:
    def __init__(
        self,
        reservations: Iterable[Reservation],
        theatre: Theatre,
        movie: Movie,
        screening_id: UUID,
    ):
        self.screening_id = screening_id
        self._reservations = set(reservations)
        self.theatre = theatre
        self.movie = movie
        self.events: list[events.Event] = []

    def make(self, reservation: Reservation):
        if self._seats_collide(reservation):
            raise SeatsCollide("Some seats are already reserved")
        self._reservations.add(reservation)
        self.events.append(events.ScreeningChanged(self.screening_id))

    def cancel(self, reservation_number: UUID):
        try:
            reservation = next(
                reservation
                for reservation in self._reservations
                if reservation.reservation_number == reservation_number
            )
        except StopIteration:
            raise ReservationDoesNotExists("Try an existing reservation")
        self._reservations.remove(reservation)
        self.events.append(events.ScreeningChanged(self.screening_id))

    def _seats_collide(self, reservation: Reservation) -> bool:
        if reservation in self._reservations:
            return False
        else:
            return bool(reservation.seats & self._seats_taken)

    @property
    def _free_seats(self) -> set[Seat]:
        return self.theatre.seats - self._seats_taken

    @property
    def _seats_taken(self) -> set[Seat]:
        seats_taken: set[Seat] = set()
        for reservation in self._reservations:
            seats_taken |= reservation.seats
        return seats_taken

    def __hash__(self) -> int:
        return hash(self.screening_id)
