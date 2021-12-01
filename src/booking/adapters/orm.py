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
    metadata,
    Column("movie_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("title", String(255)),
)

reservations = Table(
    metadata,
    Column("screening_id", ForeignKey("screenings.screening_id")),
)
