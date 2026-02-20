"""add archived_at to projects

Revision ID: d798b4fdb058
Revises: a39a193688f7
Create Date: 2026-01-06 23:40:11.193118
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  # ✅ minimal add


# revision identifiers, used by Alembic.
revision = 'd798b4fdb058'
down_revision = 'a39a193688f7'
branch_labels = None
depends_on = None


def upgrade():
    # ✅ minimal add: guard if table missing / column already exists
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("projects"):
        return

    existing_cols = {c["name"] for c in inspector.get_columns("projects")}
    if "archived_at" in existing_cols:
        return

    op.add_column(
        "projects",
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    # ✅ minimal add: safe downgrade
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("projects"):
        return

    existing_cols = {c["name"] for c in inspector.get_columns("projects")}
    if "archived_at" not in existing_cols:
        return

    op.drop_column("projects", "archived_at")

