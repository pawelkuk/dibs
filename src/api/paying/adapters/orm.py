from sqlalchemy import Table, Column, String, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import registry
from paying.domain import model

mapper_registry = registry()

payments = Table(
    "paying_payment",
    mapper_registry.metadata,
    Column("payment_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True)),
    Column("status", String(255), nullable=False),
    Column("amount", Numeric(precision=2, scale=10)),
    Column("currency", String(3), nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Payment, payments)
