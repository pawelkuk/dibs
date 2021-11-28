from typing import Iterable
from dataclasses import dataclass
from uuid import UUID, uuid4


class SeatTaken(Exception):
    pass


class SeatsCollide(Exception):
    pass


@dataclass(frozen=True)
class Seat:
    row: str
    place: int


class Theatre:
    def __init__(self, id: UUID, seats: Iterable[Seat]):
        self._id = id
        self._seats = set(seats)

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
        self._seats = set(seats)

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
        movie_id: UUID,
        screening_id: UUID,
    ):
        self.screening_id = screening_id
        self._reservations = set(reservations)
        self.theatre = theatre
        self.movie_id = movie_id

    def make(self, reservation: Reservation):
        if self._seats_collide(reservation):
            raise SeatsCollide("Some seats are already reserved")
        self._reservations.add(reservation)

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
        seats_taken = set()
        for reservation in self._reservations:
            seats_taken.union(reservation.seats)
        return seats_taken

    def __hash__(self) -> int:
        return hash(self.screening_id)