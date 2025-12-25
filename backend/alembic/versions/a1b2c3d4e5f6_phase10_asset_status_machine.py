from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "d3fe5f80b9fc"
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ Create ENUM (safe for SQLite — no-op internally)
    asset_status = sa.Enum(
        "created",
        "uploading",
        "uploaded",
        "processing",
        "ready",
        "failed",
        name="asset_status",
    )
    asset_status.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Add status column WITH constant default (SQLite-safe)
    op.add_column(
        "assets",
        sa.Column(
            "status",
            asset_status,
            nullable=False,
            server_default="ready",
        ),
    )

    # 3️⃣ Add timestamp column WITHOUT non-constant default
    op.add_column(
        "assets",
        sa.Column(
            "status_updated_at",
            sa.DateTime(timezone=True),
            nullable=True,  # TEMP nullable for SQLite
        ),
    )

    # 4️⃣ Backfill existing rows
    op.execute(
        """
        UPDATE assets
        SET
            status = CASE
                WHEN processing_error IS NOT NULL THEN 'failed'
                ELSE 'ready'
            END,
            status_updated_at = CURRENT_TIMESTAMP
        """
    )

    # 5️⃣ IMPORTANT:
    # DO NOT alter column to NOT NULL on SQLite.
    # SQLite does not support ALTER COLUMN.
    #
    # The application layer should enforce non-null going forward.


def downgrade():
    op.drop_column("assets", "status_updated_at")
    op.drop_column("assets", "status")
    sa.Enum(name="asset_status").drop(op.get_bind(), checkfirst=True)

