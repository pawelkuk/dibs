from typing import Iterable
from service_layer import unit_of_work
from uuid import UUID
from domain import model


def make_reservation(
    screening_id: UUID,
    customer_id: UUID,
    reservation_number: UUID,
    seats_data: Iterable[tuple[str, int]],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        screening: model.Screening = uow.screenings.get(screening_id=screening_id)
        seats = [model.Seat(*seat) for seat in seats_data]
        reservation = model.Reservation(seats, customer_id, reservation_number)
        screening.make(reservation=reservation)
        uow.commit()


def cancel_reservation(
    screening_id: UUID,
    reservation_number: UUID,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        screening: model.Screening = uow.screenings.get(screening_id=screening_id)
        screening.cancel(reservation_number)
        uow.commit()