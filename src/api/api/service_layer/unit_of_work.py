from __future__ import annotations
from api.adapters import repository
import abc
from api.adapters.orm import default_session_factory
from functools import partial


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, isolation_level, session_factory=default_session_factory):
        self.session_factory = partial(session_factory, isolation_level)

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
