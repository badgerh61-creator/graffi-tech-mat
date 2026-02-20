from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "a1b2c3d4e5f6"
down_revision = "d3fe5f80b9fc"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    # ✅ MINIMAL ADD: if assets table doesn't exist in this DB, skip safely
    if not inspector.has_table("assets"):
        return

    columns = [c["name"] for c in inspector.get_columns("assets")]

    # ENUM (safe)
    asset_status = sa.Enum(
        "created",
        "uploading",
        "uploaded",
        "processing",
        "ready",
        "failed",
        name="asset_status",
    )
    asset_status.create(bind, checkfirst=True)

    # status column
    if "status" not in columns:
        op.add_column(
            "assets",
            sa.Column(
                "status",
                asset_status,
                nullable=False,
                server_default="ready",
            ),
        )

    # status_updated_at column
    if "status_updated_at" not in columns:
        op.add_column(
            "assets",
            sa.Column(
                "status_updated_at",
                sa.DateTime(timezone=True),
                nullable=True,
            ),
        )

        # Backfill for existing rows
        op.execute(
            """
            UPDATE assets
            SET status_updated_at = CURRENT_TIMESTAMP
            WHERE status_updated_at IS NULL
            """
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    # ✅ MINIMAL ADD: skip safely if assets table doesn't exist
    if not inspector.has_table("assets"):
        return

    columns = [c["name"] for c in inspector.get_columns("assets")]

    if "status_updated_at" in columns:
        op.drop_column("assets", "status_updated_at")

    if "status" in columns:
        op.drop_column("assets", "status")

    sa.Enum(name="asset_status").drop(bind, checkfirst=True)

