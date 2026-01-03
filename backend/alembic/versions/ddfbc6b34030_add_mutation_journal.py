"""add mutation journal

Revision ID: ddfbc6b34030
Revises: e96b97d898c2
Create Date: 2026-01-03 08:50:03.199890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddfbc6b34030'
down_revision = 'e96b97d898c2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "mutation_journal",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("intent_type", sa.String(), nullable=False),
        sa.Column("target_type", sa.String(), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("before_state", sa.JSON(), nullable=False),
        sa.Column("after_state", sa.JSON(), nullable=False),
        sa.Column("issued_by_user_id", sa.Integer(), nullable=False),
        sa.Column(
            "issued_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("reason", sa.String(), nullable=True),
    )


def downgrade():
    op.drop_table("mutation_journal")

