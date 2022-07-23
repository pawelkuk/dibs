from django.db import models
from ticketing.domain import model


class Ticket(models.Model):
    STATUSES = [
        (k, k) for k, _ in model.TicketStatus.__dict__.items() if not k.startswith("_")
    ]
    ticket_id = models.UUIDField(primary_key=True)
    reservation_id = models.UUIDField(null=False)
    status = models.CharField(null=False, choices=STATUSES, max_length=255)
    details = models.JSONField(default=dict, null=False)
    ticket_url = models.TextField(null=True)

    def to_domain(self) -> model.Ticket:
        return model.Ticket(
            ticket_id=self.ticket_id,
            reservation_id=self.reservation_id,
            status=self.status,
            details=self.details,
            ticket_url=self.ticket_url,
        )

    @staticmethod
    def update_from_domain(ticket: model.Ticket):
        try:
            t = Ticket.objects.get(ticket_id=ticket.ticket_id)
        except Ticket.DoesNotExist:
            t = Ticket(ticket_id=ticket.ticket_id)
        t.reservation_id = ticket.reservation_id
        t.status = ticket.status.value
        t.details = ticket.details
        t.ticket_url = ticket.ticket_url
        t.save()
        return t
