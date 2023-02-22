from typing import Iterable
from booking.service_layer import unit_of_work
from uuid import UUID
from booking.domain import model
from booking import models


def make_reservation(
    screening_id: UUID,
    customer_id: UUID,
    reservation_number: UUID,
    seats_data: Iterable[tuple[str, int]],
    uow: unit_of_work.AbstractUnitOfWork,
):
    seats = [model.Seat(row=seat[0], place=int(seat[1])) for seat in seats_data]
    with uow:
        screening: model.Screening = uow.repo.get(
            model.Screening, domain_model_instance_id=screening_id
        )
        if not screening:
            raise model.ScreeningDoesNotExists(
                "You want to make a reservation for a non-existing screening"
            )
        reservation = model.Reservation(seats, customer_id, reservation_number)
        screening.make(reservation=reservation)
        reservation.seats_attr = [[s.row, s.place] for s in reservation._seats]
        uow.commit()


def cancel_reservation(
    screening_id: UUID,
    reservation_number: UUID,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        screening: model.Screening = uow.repo.get(
            model.Screening, domain_model_instance_id=screening_id
        )
        if not screening:
            raise model.ScreeningDoesNotExists(
                "You try to cancel a reservation for a non existing screening"
            )
        screening.cancel(reservation_number)
        uow.commit()


def get_screening_state(
    screening_id: UUID,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        screening: models.Screening = models.Screening.objects.get(
            screening_id=screening_id
        )
