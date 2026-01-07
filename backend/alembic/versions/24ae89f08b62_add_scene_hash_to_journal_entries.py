"""add scene_hash to journal_entries

Revision ID: 24ae89f08b62
Revises: 7309baf5f959
Create Date: 2026-01-07 13:37:09.086725
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24ae89f08b62"
down_revision = "7309baf5f959"
branch_labels = None
depends_on = None


def upgrade():
    # 1️⃣ Add column as nullable (SQLite-safe)
    op.add_column(
        "journal_entries",
        sa.Column("scene_hash", sa.String(), nullable=True),
    )

    # 2️⃣ Backfill existing rows
    op.execute(
        "UPDATE journal_entries SET scene_hash = '__legacy__' WHERE scene_hash IS NULL"
    )

    # 🚫 DO NOT ALTER NULLABILITY (SQLite limitation)
    # Enforced at application + test level instead


def downgrade():
    op.drop_column("journal_entries", "scene_hash")

