"""rename actor_id to actor_user_id in journal_entries

Revision ID: 7309baf5f959
Revises: d798b4fdb058
Create Date: 2026-01-07 13:27:05.956839
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  # ✅ minimal add


# revision identifiers, used by Alembic.
revision = '7309baf5f959'
down_revision = 'd798b4fdb058'
branch_labels = None
depends_on = None


def upgrade():
    # ✅ minimal add: guard if table missing / already renamed
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("journal_entries"):
        return

    cols = {c["name"] for c in inspector.get_columns("journal_entries")}
    if "actor_id" not in cols or "actor_user_id" in cols:
        return

    # ✅ SQLite-safe rename uses batch_alter_table
    with op.batch_alter_table("journal_entries") as batch:
        batch.alter_column(
            "actor_id",
            new_column_name="actor_user_id",
            existing_type=sa.Integer(),
        )


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("journal_entries"):
        return

    cols = {c["name"] for c in inspector.get_columns("journal_entries")}
    if "actor_user_id" not in cols or "actor_id" in cols:
        return

    with op.batch_alter_table("journal_entries") as batch:
        batch.alter_column(
            "actor_user_id",
            new_column_name="actor_id",
            existing_type=sa.Integer(),
        )

