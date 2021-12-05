from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import registry
from sqlalchemy.sql.schema import UniqueConstraint
from booking.domain import model

metadata = MetaData()
mapper_registry = registry()

screenings = Table(
    "screenings",
    mapper_registry.metadata,
    Column("screening_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("theatre_id", ForeignKey("theatres.theatre_id")),
    Column("movie_id", ForeignKey("movies.movie_id")),
)

movies = Table(
    "movies",
    mapper_registry.metadata,
    Column("movie_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(255)),
)

reservations = Table(
    "reservations",
    mapper_registry.metadata,
    Column(
        "reservation_number", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ),
    Column("screening_id", ForeignKey("screenings.screening_id")),
    Column("customer_id", UUID(as_uuid=True), nullable=False),
)

reservations_seats = Table(
    "reservations_seats",
    mapper_registry.metadata,
    Column(
        "reservation_number",
        ForeignKey("reservations.reservation_number"),
        primary_key=True,
    ),
    Column("seat_id", ForeignKey("seats.seat_id"), primary_key=True),
)

theatres_seats = Table(
    "theatres_seats",
    mapper_registry.metadata,
    Column("theatre_id", ForeignKey("theatres.theatre_id"), primary_key=True),
    Column("seat_id", ForeignKey("seats.seat_id"), primary_key=True),
)

theatres = Table(
    "theatres",
    mapper_registry.metadata,
    Column("theatre_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String(255)),
)

seats = Table(
    "seats",
    mapper_registry.metadata,
    Column("seat_id", Integer, autoincrement=True, primary_key=True),
    Column("row", String(3), nullable=False),
    Column("place", Integer, nullable=False),
    UniqueConstraint("row", "place", name="row_place_unique"),
)


def start_mappers():
    seats_mapper = mapper_registry.map_imperatively(model.Seat, seats)
    theatres_mapper = mapper_registry.map_imperatively(
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
    reservations_mapper = mapper_registry.map_imperatively(
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
    mapper_registry.map_imperatively(
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
