from typing import Iterable
from booking.service_layer import unit_of_work
from uuid import UUID
from booking.domain import model


def make_reservation(
    screening_id: UUID,
    customer_id: UUID,
    reservation_number: UUID,
    seats_data: Iterable[tuple[str, int]],
    uow: unit_of_work.AbstractUnitOfWork,
):
    seats = [model.Seat(*seat) for seat in seats_data]
    with uow:
        reservation = model.Reservation(seats, customer_id, reservation_number)
        screening: model.Screening = uow.screenings.get(screening_id=screening_id)
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
