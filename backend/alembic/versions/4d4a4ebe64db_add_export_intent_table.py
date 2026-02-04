"""add export intent table

Revision ID: 4d4a4ebe64db
Revises: 24ae89f08b62
Create Date: 2026-02-04 18:58:32.682833
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "4d4a4ebe64db"
down_revision = "24ae89f08b62"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # --- Phase E / Tier 1.2 ---
    # Export INTENT only (no execution)

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

    op.create_index("ix_exports_id", "exports", ["id"])

    # 🔗 Bridge intent → execution (Phase M+)
    op.create_foreign_key(
        "fk_export_jobs_export_request_id_exports",
        "export_jobs",
        "exports",
        ["export_request_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # 🚫 Historical tables are NEVER recreated
    # 🚫 Only reverse what this migration introduced

    op.drop_constraint(
        "fk_export_jobs_export_request_id_exports",
        "export_jobs",
        type_="foreignkey",
    )

    op.drop_index("ix_exports_id", table_name="exports")
    op.drop_table("exports")

