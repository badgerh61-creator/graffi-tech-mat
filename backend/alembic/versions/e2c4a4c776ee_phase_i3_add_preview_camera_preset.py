"""
Phase I.3 — add preview camera preset to models

Revision ID: e2c4a4c776ee
Revises: 4c6b6a5d23b5
Create Date: 2026-01-XX
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  # ✅ minimal add

# revision identifiers, used by Alembic.
revision = "e2c4a4c776ee"
down_revision = "4c6b6a5d23b5"
branch_labels = None
depends_on = None


def upgrade():
    # ✅ minimal add: guard if table missing / already applied
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("models"):
        return

    cols = {c["name"] for c in inspector.get_columns("models")}
    if "preview_camera_preset_id" in cols:
        # Column already exists; don't try to re-add or alter defaults.
        return

    # Phase I.3 — editor metadata only (SQLite-safe)
    op.add_column(
        "models",
        sa.Column(
            "preview_camera_preset_id",
            sa.String(),
            nullable=False,
            server_default="front_iso",
        ),
    )

    # Remove server default after existing rows are backfilled
    op.alter_column(
        "models",
        "preview_camera_preset_id",
        server_default=None,
    )


def downgrade():
    # ✅ minimal add: safe downgrade
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("models"):
        return

    cols = {c["name"] for c in inspector.get_columns("models")}
    if "preview_camera_preset_id" not in cols:
        return

    op.drop_column("models", "preview_camera_preset_id")

