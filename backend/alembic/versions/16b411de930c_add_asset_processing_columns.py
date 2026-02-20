from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# =============================
# Alembic revision identifiers
# =============================

revision = "16b411de930c"
down_revision = "d3fe5f80b9fc"  # audit logs revision
branch_labels = None
depends_on = None


def upgrade():
    # ✅ MINIMAL ADD: make idempotent + safe when assets table doesn't exist
    bind = op.get_bind()
    inspector = inspect(bind)

    if not inspector.has_table("assets"):
        return

    existing_cols = {c["name"] for c in inspector.get_columns("assets")}

    # Add processing timestamp (only if missing)
    if "processed_at" not in existing_cols:
        op.add_column(
            "assets",
            sa.Column(
                "processed_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
        )

    # Add processing error field (only if missing)
    if "processing_error" not in existing_cols:
        op.add_column(
            "assets",
            sa.Column(
                "processing_error",
                sa.Text(),
                nullable=True,
            ),
        )


def downgrade():
    # ✅ MINIMAL ADD: only drop if table + column exist (safe on partially-applied DBs)
    bind = op.get_bind()
    inspector = inspect(bind)

    if not inspector.has_table("assets"):
        return

    existing_cols = {c["name"] for c in inspector.get_columns("assets")}

    if "processing_error" in existing_cols:
        op.drop_column("assets", "processing_error")

    if "processed_at" in existing_cols:
        op.drop_column("assets", "processed_at")

