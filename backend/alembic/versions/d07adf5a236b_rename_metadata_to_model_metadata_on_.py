"""rename metadata to model_metadata on models

Revision ID: d07adf5a236b
Revises: 56167f9c09ba
Create Date: 2025-12-13 18:03:44.484054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd07adf5a236b'
down_revision = '56167f9c09ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
