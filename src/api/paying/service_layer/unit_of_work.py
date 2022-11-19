from __future__ import annotations
import abc
from paying.adapters import repository
from django.db import transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from booking import config


class AbstractUnitOfWork(abc.ABC):
    payments: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.payments = repository.DjangoRepository()
        transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)

    def commit(self):
        for payment in self.payments.seen:
            self.payments.update(payment)
        transaction.commit()

    def rollback(self):
        transaction.rollback()


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri("postgres_paying"),
        isolation_level="REPEATABLE READ",
        future=True,
        echo=True,
    )
)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.payments = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
