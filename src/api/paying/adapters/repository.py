import abc
from uuid import UUID
from paying.domain import model
from paying import models as django_models


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set[model.Payment] = set()

    def add(self, payment: model.Payment):
        self.seen.add(payment)

    def get(self, payment_id: UUID) -> model.Payment:
        p = self._get(payment_id)
        if p:
            self.seen.add(p)
        return p

    @abc.abstractmethod
    def _get(self, payment_id: UUID) -> model.Payment:
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def add(self, payment: model.Payment):
        super().add(payment)
        self.update(payment)

    def update(self, payment: model.Payment):
        django_models.Payment.update_from_domain(payment)

    def _get(self, payment_id: UUID) -> model.Payment:
        return (
            django_models.Payment.objects.filter(payment_id=payment_id)
            .first()
            .to_domain()
        )

    def list(self) -> list[model.Payment]:
        return [p.to_domain() for p in django_models.Payment.objects.all()]


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, payment):
        self.session.add(payment)

    def _get(self, payment_id: UUID) -> model.Payment:
        return (
            self.session.query(model.Payment).filter_by(payment_id=payment_id).first()
        )
