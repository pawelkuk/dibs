from enum import auto
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.sql.schema import UniqueConstraint
from booking.domain import model

metadata = MetaData()

screenings = Table(
    "screenings",
    metadata,
    Column("screening_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("theatre_id", ForeignKey("theatres.theatre_id")),
    Column("movie_id", ForeignKey("movies.movie_id")),
)

movies = Table(
    "movies",
    metadata,
    Column("movie_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(255)),
)

reservations = Table(
    "reservations",
    metadata,
    Column(
        "reservation_number", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ),
    Column("screening_id", ForeignKey("screenings.screening_id")),
    Column("customer_id", UUID(as_uuid=True), nullable=False),
)

reservations_seats = Table(
    "reservations_seats",
    metadata,
    Column(
        "reservation_number",
        ForeignKey("reservations.reservation_number"),
        primary_key=True,
    ),
    Column("seat_id", ForeignKey("seats.seat_id"), primary_key=True),
)

theatres_seats = Table(
    "theatres_seats",
    metadata,
    Column("theatre_id", ForeignKey("theatres.theatre_id"), primary_key=True),
    Column("seat_id", ForeignKey("seats.seat_id"), primary_key=True),
)

theatres = Table(
    "theatres",
    metadata,
    Column("theatre_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(255)),
)

seats = Table(
    "seats",
    metadata,
    Column("seat_id", Integer, autoincrement=True, primary_key=True),
    Column("row", String(3), nullable=False),
    Column("place", Integer, nullable=False),
    UniqueConstraint("row", "place", name="row_place_unique"),
)


def start_mappers():
    seats_mapper = mapper(model.Seat, seats)
    theatres_mapper = mapper(
        model.Theatre,
        theatres,
        properties={
            "_seats": relationship(
                seats_mapper,
                secondary=theatres_seats,
                collection_class=set,
            )
        },
    )
    reservations_mapper = mapper(
        model.Reservation,
        reservations,
        properties={
            "_seats": relationship(
                seats_mapper,
                secondary=reservations_seats,
                collection_class=set,
            )
        },
    )
    mapper(
        model.Screening,
        screenings,
        properties={
            "_reservations": relationship(
                reservations_mapper,
                collection_class=set,
            ),
            "theatre": relationship(theatres_mapper),
        },
    )
