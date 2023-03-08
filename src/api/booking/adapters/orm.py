from sqlalchemy import Table, Column, String, ForeignKey, ARRAY, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import registry
from booking.domain import model

mapper_registry = registry()

screenings = Table(
    "booking_screening",
    mapper_registry.metadata,
    Column("screening_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("theatre_id", ForeignKey("booking_theatre.theatre_id")),
    Column("movie_id", ForeignKey("booking_movie.movie_id")),
)

movies = Table(
    "booking_movie",
    mapper_registry.metadata,
    Column("movie_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(1023)),
)

reservations = Table(
    "booking_reservation",
    mapper_registry.metadata,
    Column(
        "reservation_number", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ),
    Column("screening_id", ForeignKey("booking_screening.screening_id")),
    Column("customer_id", UUID(as_uuid=True), nullable=False),
)

seats = Table(
    "booking_seat",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("row", String(3)),
    Column("place", Integer),
    Column("screening_id", ForeignKey("booking_screening.screening_id")),
    Column("reservation_id", ForeignKey("booking_reservation.reservation_number")),
)

theatres = Table(
    "booking_theatre",
    mapper_registry.metadata,
    Column("theatre_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("seats", ARRAY(String, dimensions=2)),
)


def start_mappers():
    movies_mapper = mapper_registry.map_imperatively(model.Movie, movies)
    theatres_mapper = mapper_registry.map_imperatively(model.Theatre, theatres)
    seats_mapper = mapper_registry.map_imperatively(model.Seat, seats)
    reservations_mapper = mapper_registry.map_imperatively(
        model.Reservation,
        reservations,
        properties={
            "_seats2": relationship(seats_mapper, collection_class=set, lazy="joined")
        },
    )
    mapper_registry.map_imperatively(
        model.Screening,
        screenings,
        properties={
            "movie": relationship(movies_mapper),
            "theatre": relationship(theatres_mapper),
            "_reservations": relationship(
                reservations_mapper,
                collection_class=set,
            ),
        },
    )