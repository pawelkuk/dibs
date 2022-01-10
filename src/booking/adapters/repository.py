import abc
from uuid import UUID
from booking.domain import model
from djangoproject.alloc import models as django_models


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, screening: model.Screening):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, screening_id: UUID) -> model.Screening:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, screening: model.Screening):
        self.session.add(screening)

    def get(self, screening_id: UUID) -> model.Screening:
        return (
            self.session.query(model.Screening)
            .filter_by(screening_id=screening_id)
            .first()
        )

class FakeRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, screening: model.Screening):
        self.session[screening.screening_id] = screening

    def get(self, screening_id: UUID) -> model.Screening:
        return self.session[screening_id]

class DjangoRepository(AbstractRepository):
    def add(self, batch):
        super().add(batch)
        self.update(batch)

    def update(self, batch):
        django_models.Batch.update_from_domain(batch)

    def _get(self, reference):
        return (
            django_models.Batch.objects.filter(reference=reference).first().to_domain()
        )

    def list(self):
        return [b.to_domain() for b in django_models.Batch.objects.all()]
