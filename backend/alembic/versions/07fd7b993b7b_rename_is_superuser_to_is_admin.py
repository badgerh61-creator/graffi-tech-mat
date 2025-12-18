"""rename is_superuser to is_admin

Revision ID: 07fd7b993b7b
Revises: 875bc8bec441
Create Date: 2025-12-14 15:00:03.001830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07fd7b993b7b'
down_revision = '875bc8bec441'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
