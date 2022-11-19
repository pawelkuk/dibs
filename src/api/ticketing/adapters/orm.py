from sqlalchemy import Table, Column, String, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import registry
from ticketing.domain import model

mapper_registry = registry()

tickets = Table(
    "ticketing_ticket",
    mapper_registry.metadata,
    Column("ticket_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("reservation_id", UUID(as_uuid=True), nullable=False),
    Column("status", String(255), nullable=False),
    Column("details", JSON(none_as_null=True), nullable=False),
    Column("ticket_url", String(255), nullable=True),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Ticket, tickets)
