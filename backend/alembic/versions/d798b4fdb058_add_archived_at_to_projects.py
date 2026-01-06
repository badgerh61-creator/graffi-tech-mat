"""add archived_at to projects

from alembic import op
import sqlalchemy as sa

Revision ID: d798b4fdb058
Revises: a39a193688f7
Create Date: 2026-01-06 23:40:11.193118

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd798b4fdb058'
down_revision = 'a39a193688f7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "projects",
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_column("projects", "archived_at")

















