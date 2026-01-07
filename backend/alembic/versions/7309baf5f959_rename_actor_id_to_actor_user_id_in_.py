"""rename actor_id to actor_user_id in journal_entries

Revision ID: 7309baf5f959
Revises: d798b4fdb058
Create Date: 2026-01-07 13:27:05.956839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7309baf5f959'
down_revision = 'd798b4fdb058'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "journal_entries",
        "actor_id",
        new_column_name="actor_user_id",
    )


def downgrade():
    op.alter_column(
        "journal_entries",
        "actor_user_id",
        new_column_name="actor_id",
    )
