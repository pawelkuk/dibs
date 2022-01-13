import abc
from uuid import UUID
from booking.domain import model
from booking import models as django_models


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set[model.Screening] = set()

    def add(self, screening: model.Screening):
        self.seen.add(screening)

    def get(self, screening_id: UUID) -> model.Screening:
        p = self._get(screening_id)
        if p:
            self.seen.add(p)
        return p

    @abc.abstractmethod
    def _get(self, screening_id: UUID) -> model.Screening:
        raise NotImplementedError


class DjangoRepository(AbstractRepository):
    def add(self, screening: model.Screening):
        super().add(screening)
        self.update(screening)

    def update(self, screening: model.Screening):
        django_models.Screening.update_from_domain(screening)

    def _get(self, screening_id: UUID) -> model.Screening:
        return (
            django_models.Screening.objects.filter(screening_id=screening_id)
            .first()
            .to_domain()
        )

    def list(self) -> list[model.Screening]:
        return [s.to_domain() for s in django_models.Screening.objects.all()]
