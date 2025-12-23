"""default datetime

Revision ID: c2a8bfade94e
Revises: 05444ec04b02
Create Date: 2025-12-24 07:45:49.235945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a8bfade94e'
down_revision: Union[str, Sequence[str], None] = '05444ec04b02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
