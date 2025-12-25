"""rename_audit_metadata_to_extra

Revision ID: b398c9555cf4
Revises: d3fe5f80b9fc
Create Date: 2025-12-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers
revision = "b398c9555cf4"
down_revision = "d3fe5f80b9fc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [c["name"] for c in inspector.get_columns("audit_logs")]

    # Only rename if metadata exists and extra does NOT
    if "metadata" in columns and "extra" not in columns:
        with op.batch_alter_table("audit_logs") as batch:
            batch.alter_column(
                "metadata",
                new_column_name="extra",
                existing_type=sa.JSON(),
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [c["name"] for c in inspector.get_columns("audit_logs")]

    if "extra" in columns and "metadata" not in columns:
        with op.batch_alter_table("audit_logs") as batch:
            batch.alter_column(
                "extra",
                new_column_name="metadata",
                existing_type=sa.JSON(),
            )

