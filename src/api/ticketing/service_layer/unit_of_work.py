from __future__ import annotations
import abc
from ticketing.adapters import repository
from django.db import transaction


class AbstractUnitOfWork(abc.ABC):
    tickets: repository.AbstractRepository

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
        self.tickets = repository.DjangoRepository()
        transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)

    def commit(self):
        for ticket in self.tickets.seen:
            self.tickets.update(ticket)
        transaction.commit()

    def rollback(self):
        transaction.rollback()
