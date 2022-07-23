from __future__ import annotations
import abc
from paying.adapters import repository
from django.db import transaction


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
        for payment in self.payments:
            self.payments.update(payment)
        transaction.commit()

    def rollback(self):
        transaction.rollback()
