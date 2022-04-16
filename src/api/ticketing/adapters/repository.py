import abc
from uuid import UUID
from ticketing.domain import model
from ticketing import models as django_models


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set[model.Ticket] = set()

    def add(self, ticket: model.Ticket):
        self.seen.add(ticket)

    def get(self, ticket_id: UUID) -> model.Ticket:
        p = self._get(ticket_id)
        if p:
            self.seen.add(p)
        return p

    @abc.abstractmethod
    def _get(self, ticket_id: UUID) -> model.Ticket:
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def add(self, ticket: model.Ticket):
        super().add(ticket)
        self.update(ticket)

    def update(self, ticket: model.Ticket):
        django_models.Ticket.update_from_domain(ticket)

    def _get(self, ticket_id: UUID) -> model.Ticket:
        return (
            django_models.Ticket.objects.filter(ticket_id=ticket_id).first().to_domain()
        )

    def list(self) -> list[model.Ticket]:
        return [t.to_domain() for t in django_models.Ticket.objects.all()]
