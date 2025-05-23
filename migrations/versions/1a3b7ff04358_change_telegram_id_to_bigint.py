"""change_telegram_id_to_bigint

Revision ID: 1a3b7ff04358
Revises: c1c38e807b18
Create Date: 2025-05-23 12:44:51.206641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a3b7ff04358'
down_revision: Union[str, None] = 'c1c38e807b18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
