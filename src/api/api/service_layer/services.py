from typing import Iterable
from api.service_layer import unit_of_work
from uuid import UUID
from booking.domain import model as booking_model
from ticketing.domain import model as ticketing_model
from paying.domain import model as paying_model


def dibs(
    screening_id: UUID,
    customer_id: UUID,
    reservation_number: UUID,
    seats_data: Iterable[tuple[str, int]],
    amount: str,
    currency: paying_model.Currency,
    payment_success_rate: float,
    ticketing_success_rate: float,
    details: dict,
    uow: unit_of_work.SqlAlchemyUnitOfWork,
):
    seats = [booking_model.Seat(row=seat[0], place=int(seat[1])) for seat in seats_data]
    with uow:
        screening: booking_model.Screening = uow.repo.get(
            booking_model.Screening, domain_model_instance_id=screening_id
        )
        if not screening:
            raise booking_model.ScreeningDoesNotExists(
                "You want to make a reservation for a non-existing screening"
            )
        reservation = booking_model.Reservation(seats, customer_id, reservation_number)
        import bpdb

        bpdb.set_trace()
        screening.make(reservation=reservation)

        payment = paying_model.Payment(
            amount=amount, currency=currency, user_id=customer_id
        )
        payment_id = payment.pay(payment_success_rate)
        uow.repo.add(payment=payment)
        ticket = ticketing_model.Ticket(
            details=details, reservation_id=reservation.reservation_number
        )
        ticket_id = ticket.render(ticketing_success_rate)
        uow.repo.add(ticket=ticket)
        uow.commit()
    return {
        "payment_id": payment_id,
        "ticket_id": ticket_id,
        "reservation_number": reservation_number,
    }
