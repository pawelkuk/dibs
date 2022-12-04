from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from booking import config
from booking.adapters import orm as booking_orm
from paying.adapters import orm as paying_orm
from ticketing.adapters import orm as ticketing_orm


def default_session_factory():
    paying_engine = create_engine(
        config.get_postgres_uri("postgres_paying"),
        isolation_level=config.SQL_ALCHEMY_ISOLATION_LEVEL,
        future=True,
        echo=True,
    )
    ticketing_engine = create_engine(
        config.get_postgres_uri("postgres_ticketing"),
        isolation_level=config.SQL_ALCHEMY_ISOLATION_LEVEL,
        future=True,
        echo=True,
    )
    booking_engine = create_engine(
        config.get_postgres_uri("postgres_booking"),
        isolation_level=config.SQL_ALCHEMY_ISOLATION_LEVEL,
        future=True,
        echo=True,
    )

    Session = sessionmaker(twophase=True)
    Session.configure(
        binds={
            paying_orm.payments: paying_engine,
            ticketing_orm.tickets: ticketing_engine,
            booking_orm.movies: booking_engine,
            booking_orm.reservations: booking_engine,
            booking_orm.screenings: booking_engine,
            booking_orm.theatres: booking_engine,
        }
    )
    return Session()