"""add_document_path_to_tratamiento

Revision ID: 39b893ef230d
Revises: d2d45b2cfc6c
Create Date: 2025-12-03 19:32:21.551815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39b893ef230d'
down_revision: Union[str, Sequence[str], None] = 'd2d45b2cfc6c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
