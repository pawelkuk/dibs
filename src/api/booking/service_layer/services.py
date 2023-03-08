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
    with uow:
        screening: model.Screening = uow.repo.get(
            model.Screening, domain_model_instance_id=screening_id
        )
        if not screening:
            raise model.ScreeningDoesNotExists(
                "You want to make a reservation for a non-existing screening"
            )
        seats = [
            model.Seat(
                id=None,
                row=seat[0],
                place=int(seat[1]),
                screening_id=screening.screening_id,
                reservation_id=None,
            )
            for seat in seats_data
        ]
        reservation = model.Reservation(seats, customer_id, reservation_number)
        screening.make(reservation=reservation)
        reservation._seats2.update(reservation._seats)
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
