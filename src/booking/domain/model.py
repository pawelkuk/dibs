from typing import Iterable
from dataclasses import dataclass
from uuid import UUID, uuid4


class SeatTaken(Exception):
    pass


@dataclass(frozen=True)
class Seat:
    row: str
    place: int


class Theatre:
    def __init__(self, id: UUID, seats: Iterable[Seat]):
        self._id = id
        self._seats = set(seats)


class Cart:
    def __init__(self, seats: Iterable[Seat], customer_id: UUID):
        self._seats = set(seats)
        self.customer_id = customer_id

    def add(self, seat: Seat):
        if True:  # seat is available
            self._seats.add(seat)
        else:
            raise SeatTaken("Choose other seat")

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

    # this should be a domain layer function (check nomenclature)
    @classmethod
    def from_cart(cls, cart: Cart):
        return cls(cart.seats, cart.customer_id)


class Screening:
    def __init__(
        self, reservations: Iterable[Reservation], theatre: Theatre, movie_id: UUID
    ):
        self._reservations = set(reservations)
        self.theatre = theatre
        self.movie_id = movie_id
