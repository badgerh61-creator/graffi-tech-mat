"""Phase F2.1 — add organizations core tables

Revision ID: afe3fa68ab1f
Revises: e554187
Create Date: 2025-12-26
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "afe3fa68ab1f"
down_revision = "e554187"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "organization_members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "organization_id",
            sa.Integer(),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.String(),
            nullable=False,
            server_default="member",
        ),
        sa.UniqueConstraint(
            "organization_id",
            "user_id",
            name="uq_org_member",
        ),
    )


def downgrade():
    op.drop_table("organization_members")
    op.drop_table("organizations")
