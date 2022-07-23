from enum import Enum
from uuid import UUID, uuid4
import random


class TicketRenderError(Exception):
    pass


class TicketStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"


class Ticket:
    def __init__(
        self,
        reservation_id: UUID,
        details: dict,
        ticket_id: UUID = None,
        status: str = None,
        ticket_url: str = None,
    ) -> None:
        self.ticket_id = ticket_id
        self.reservation_id = reservation_id
        self.status = status
        self.details = details
        self.ticket_url = ticket_url

    def render(self) -> str:
        if self.ticket_url and self.status == TicketStatus.SUCCESS:
            return self.ticket_url
        elif not self.ticket_id or not self.reservation_id or not self.details:
            raise TicketRenderError("Insufficient information to render ticket!")
        elif random.random() < 0.99:
            # Happy path
            self.ticket_url = Ticket.generate_ticket_url()
            self.status = TicketStatus.SUCCESS
        else:
            self.status = TicketStatus.FAILED
            raise TicketRenderError("Unknown error. Try again!")

        return self.ticket_url

    @staticmethod
    def generate_ticket_url():
        return f"/dibs_tickets/some-s3-path/{uuid4()}.pdf"
