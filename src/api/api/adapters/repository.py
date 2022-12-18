import abc
from uuid import UUID
from typing import Any
from booking.domain import model as booking_model
from ticketing.domain import model as ticketing_model
from paying.domain import model as paying_model

class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set = set()

    def add(self, domain_model_instance: Any):
        self._add(domain_model_instance)
        self.seen.add(domain_model_instance)

    def get(self, domain_model_class: Any, domain_model_instance_id: UUID) -> Any:
        p = self._get(domain_model_class, domain_model_instance_id)
        if p:
            self.seen.add(p)
        return p

    @abc.abstractmethod
    def _get(self, domain_model_class: Any, domain_model_instance_id: UUID) -> Any:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, domain_model_instance):
        match domain_model_instance:
            case booking_model.Screening():
                pass
            case paying_model.Payment() | ticketing_model.Ticket():
                domain_model_instance.status = domain_model_instance.status.value
            case _:
                raise TypeError("This model is not supported")
        self.session.add(domain_model_instance)

    def _get(self, domain_model_class: Any, domain_model_instance_id: UUID) -> Any:
        match domain_model_class:
            case booking_model.Screening:
                lookup_field = "screening_id"
            case paying_model.Payment:
                lookup_field = "payment_id"
            case ticketing_model.Ticket:
                lookup_field = "ticket_id"
            case _:
                raise TypeError("This model is not supported")
            
        res = (
            self.session.query(domain_model_class)
            .filter_by(**{lookup_field:domain_model_instance_id})
            .first()
        )
        match domain_model_class:
            case booking_model.Screening:
                res.events = []
                for r in res._reservations:
                    r._seats = {booking_model.Seat(x[0], int(x[1])) for x in r.seats_attr}
            case _:
                pass

        return res