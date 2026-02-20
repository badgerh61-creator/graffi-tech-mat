"""add export intent table

Revision ID: 4d4a4ebe64db
Revises: 24ae89f08b62
Create Date: 2026-02-04 18:58:32.682833
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  # ✅ minimal add

# revision identifiers, used by Alembic.
revision = "4d4a4ebe64db"
down_revision = "24ae89f08b62"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Phase E / Tier 1.2 ---
    # Export INTENT only (no execution)

    bind = op.get_bind()  # ✅ minimal add
    inspector = inspect(bind)

    # ✅ minimal add: idempotent guard (prevents re-create on partially built DBs)
    if not inspector.has_table("exports"):
        op.create_table(
            "exports",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "snapshot_id",
                sa.Integer(),
                sa.ForeignKey("rendered_snapshots.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column("export_type", sa.String(), nullable=False),
            sa.Column("format", sa.String(), nullable=False),
            sa.Column("resolution", sa.String(), nullable=False),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column(
                "created_by",
                sa.Integer(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
        )

    # ✅ minimal add: index idempotency
    existing_indexes = {ix["name"] for ix in inspector.get_indexes("exports")} if inspector.has_table("exports") else set()
    if "ix_exports_id" not in existing_indexes:
        op.create_index("ix_exports_id", "exports", ["id"])

    # 🔗 Bridge intent → execution (Phase M+)
    # ✅ SQLite cannot ALTER constraints. Only add this FK on DBs that support it.
    # SQLite-safe FK bridge is handled later via batch migrations.
    if bind.dialect.name != "sqlite":
        # ✅ minimal add: guard prereq table exists
        inspector = inspect(bind)  # refresh
        if inspector.has_table("export_jobs") and inspector.has_table("exports"):
            op.create_foreign_key(
                "fk_export_jobs_export_request_id_exports",
                "export_jobs",
                "exports",
                ["export_request_id"],
                ["id"],
                ondelete="CASCADE",
            )


def downgrade() -> None:
    bind = op.get_bind()  # ✅ minimal add
    inspector = inspect(bind)

    # 🚫 Historical tables are NEVER recreated
    # 🚫 Only reverse what this migration introduced

    # ✅ minimal add: SQLite can't drop constraints via ALTER either; skip safely
    if bind.dialect.name != "sqlite":
        inspector = inspect(bind)
        if inspector.has_table("export_jobs"):
            # drop constraint only if present
            # (best-effort: Alembic doesn't have a clean "exists" check for constraints)
            op.drop_constraint(
                "fk_export_jobs_export_request_id_exports",
                "export_jobs",
                type_="foreignkey",
            )

    if inspector.has_table("exports"):
        # drop index if exists
        existing_indexes = {ix["name"] for ix in inspector.get_indexes("exports")}
        if "ix_exports_id" in existing_indexes:
            op.drop_index("ix_exports_id", table_name="exports")

        op.drop_table("exports")

