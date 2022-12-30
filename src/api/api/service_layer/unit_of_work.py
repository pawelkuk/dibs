from __future__ import annotations
from api.adapters import repository
import abc
from api.adapters.orm import default_session_factory
from functools import partial
from booking.adapters import publisher


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()
        self.publish_events()

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    def publish_events(self):
        for instance in self.repo.seen:
            if not hasattr(instance, "events"):
                continue
            while instance.events:
                event = instance.events.pop(0)
                self.messagebus.publish(event)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, isolation_level, session_factory=default_session_factory):
        self.session_factory = partial(session_factory, isolation_level)

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = repository.SqlAlchemyRepository(self.session)
        self.messagebus = publisher.CeleryPublisher()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
