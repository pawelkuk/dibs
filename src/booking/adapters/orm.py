from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
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
    Column("reservation_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("screening_id", ForeignKey("screenings.screening_id")),
    Column("customer_id", UUID(as_uuid=True), nullable=False),
)

reservations_seats = Table(
    "reservations_seats",
    metadata,
    Column(
        "reservation_id", ForeignKey("reservations.reservation_id"), primary_key=True
    ),
    Column("row", ForeignKey("seats.row"), primary_key=True),
    Column("place", ForeignKey("seats.place"), primary_key=True),
)

theatres_seats = Table(
    "theatres_seats",
    metadata,
    Column("theatre_id", ForeignKey("theatres.theatre_id"), primary_key=True),
    Column("row", ForeignKey("seats.row"), primary_key=True),
    Column("place", ForeignKey("seats.place"), primary_key=True),
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
    Column("row", String(3), nullable=False),
    Column("place", Integer, nullable=False),
)