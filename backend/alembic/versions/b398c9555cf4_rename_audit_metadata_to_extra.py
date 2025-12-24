"""rename_audit_metadata_to_extra

Revision ID: b398c9555cf4
Revises: d3fe5f80b9fc
Create Date: 2025-12-24 11:52:01.651617
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b398c9555cf4"
down_revision = "d3fe5f80b9fc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite-safe column rename
    with op.batch_alter_table("audit_logs") as batch:
        batch.alter_column(
            "metadata",
            new_column_name="extra",
            existing_type=sa.JSON(),
        )


def downgrade() -> None:
    with op.batch_alter_table("audit_logs") as batch:
        batch.alter_column(
            "extra",
            new_column_name="metadata",
            existing_type=sa.JSON(),
        )
