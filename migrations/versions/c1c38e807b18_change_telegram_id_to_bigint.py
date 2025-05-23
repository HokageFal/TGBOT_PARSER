"""change_telegram_id_to_bigint

Revision ID: c1c38e807b18
Revises: c37fd2aa3307
Create Date: 2025-05-23 12:29:10.980877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1c38e807b18'
down_revision: Union[str, None] = 'c37fd2aa3307'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
