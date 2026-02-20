"""add asset visibility flag

Revision ID: 4c6b6a5d23b5
Revises: ddfbc6b34030
Create Date: 2026-01-03 14:32:17.681549
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  # ✅ minimal add


revision = '4c6b6a5d23b5'
down_revision = 'ddfbc6b34030'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ✅ minimal add: only run if table exists (baseline path may not have assets)
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("assets"):
        return

    # ✅ minimal add: idempotent if column already exists
    existing_cols = {c["name"] for c in inspector.get_columns("assets")}
    if "is_visible" in existing_cols:
        return

    # Phase I.2 — metadata-only visibility flag
    # SQLite-safe: keep server_default
    op.add_column(
        "assets",
        sa.Column(
            "is_visible",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    # ✅ minimal add: safe downgrade if table/column missing
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("assets"):
        return

    existing_cols = {c["name"] for c in inspector.get_columns("assets")}
    if "is_visible" not in existing_cols:
        return

    op.drop_column("assets", "is_visible")

