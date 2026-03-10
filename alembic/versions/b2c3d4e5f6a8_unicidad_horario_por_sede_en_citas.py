"""unicidad horario por sede en citas

Revision ID: b2c3d4e5f6a8
Revises: a1b2c3d4e5f7
Create Date: 2026-03-09 11:20:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a8"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_appointments_scheduled_at", "appointments", type_="unique")
    op.create_unique_constraint(
        "uq_appointments_sede_scheduled_at",
        "appointments",
        ["sede", "scheduled_at"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_appointments_sede_scheduled_at", "appointments", type_="unique")
    op.create_unique_constraint("uq_appointments_scheduled_at", "appointments", ["scheduled_at"])
