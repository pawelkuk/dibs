"""create models

Revision ID: 81ccba415a69
Revises: 
Create Date: 2021-12-04 22:37:05.749382

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '81ccba415a69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('movie_id')
    )
    op.create_table('seats',
    sa.Column('seat_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('row', sa.String(length=3), nullable=False),
    sa.Column('place', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('seat_id'),
    sa.UniqueConstraint('row', 'place', name='row_place_unique')
    )
    op.create_table('theatres',
    sa.Column('theatre_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('theatre_id')
    )
    op.create_table('screenings',
    sa.Column('screening_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('theatre_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('movie_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], ),
    sa.ForeignKeyConstraint(['theatre_id'], ['theatres.theatre_id'], ),
    sa.PrimaryKeyConstraint('screening_id')
    )
    op.create_table('theatres_seats',
    sa.Column('theatre_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('seat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['seat_id'], ['seats.seat_id'], ),
    sa.ForeignKeyConstraint(['theatre_id'], ['theatres.theatre_id'], ),
    sa.PrimaryKeyConstraint('theatre_id', 'seat_id')
    )
    op.create_table('reservations',
    sa.Column('reservation_number', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('screening_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['screening_id'], ['screenings.screening_id'], ),
    sa.PrimaryKeyConstraint('reservation_number')
    )
    op.create_table('reservations_seats',
    sa.Column('reservation_number', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('seat_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['reservation_number'], ['reservations.reservation_number'], ),
    sa.ForeignKeyConstraint(['seat_id'], ['seats.seat_id'], ),
    sa.PrimaryKeyConstraint('reservation_number', 'seat_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations_seats')
    op.drop_table('reservations')
    op.drop_table('theatres_seats')
    op.drop_table('screenings')
    op.drop_table('theatres')
    op.drop_table('seats')
    op.drop_table('movies')
    # ### end Alembic commands ###