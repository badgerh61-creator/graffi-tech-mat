"""merge migration heads

Revision ID: 875bc8bec441
Revises: d07adf5a236b, xxxx
Create Date: 2025-12-13 18:22:35.004306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '875bc8bec441'
down_revision = ('d07adf5a236b', 'xxxx')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
