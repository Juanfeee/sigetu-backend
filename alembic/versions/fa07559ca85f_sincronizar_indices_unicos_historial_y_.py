"""sincronizar_indices_unicos_historial_y_tokens

Revision ID: fa07559ca85f
Revises: 5fedfbdef732
Create Date: 2026-03-06 09:40:56.577052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa07559ca85f'
down_revision: Union[str, Sequence[str], None] = '5fedfbdef732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
