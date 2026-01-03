"""add asset visibility flag

Revision ID: 4c6b6a5d23b5
Revises: ddfbc6b34030
Create Date: 2026-01-03 14:32:17.681549
"""

from alembic import op
import sqlalchemy as sa


revision = '4c6b6a5d23b5'
down_revision = 'ddfbc6b34030'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Phase I.2 — metadata-only visibility flag
    # SQLite-safe: keep server_default
    op.add_column(
        "assets",
        sa.Column(
            "is_visible",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )


def downgrade() -> None:
    op.drop_column("assets", "is_visible")

