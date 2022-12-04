import abc
from uuid import UUID
from typing import Any


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set = set()

    def add(self, domain_model_instance: Any):
        self._add(domain_model_instance)
        self.seen.add(domain_model_instance)

    def get(self, domain_model_instance_id: UUID) -> Any:
        p = self._get(domain_model_instance_id)
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
        self.session.add(domain_model_instance)

    def _get(self, domain_model_class: Any, domain_model_instance_id: UUID) -> Any:
        return (
            self.session.query(domain_model_class)
            .filter_by(pk=domain_model_instance_id)
            .first()
        )