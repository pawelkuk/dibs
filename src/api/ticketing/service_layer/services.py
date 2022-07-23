from ticketing.service_layer import unit_of_work
from uuid import UUID
from ticketing.domain import model


def render_ticket(
    reservation_id: UUID,
    details: dict,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        ticket = model.Ticket(details=details, reservation_id=reservation_id)
        ticket_id = ticket.render()
        uow.tickets.add(ticket=ticket)
        uow.commit()
    return ticket_id
