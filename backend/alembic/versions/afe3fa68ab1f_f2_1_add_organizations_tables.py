# backend/alembic/versions/afe3fa68ab1f_f2_1_add_organizations_tables.py

"""
Phase F2.1 — add organizations core tables

Revision ID: afe3fa68ab1f
Revises: b264282e1afa
Create Date: 2025-12-26
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect  # ✅ minimal add


# revision identifiers, used by Alembic.
revision = "afe3fa68ab1f"
down_revision = "b264282e1afa"
branch_labels = None
depends_on = None


def upgrade():
    # ✅ minimal add: idempotent creates + prerequisite guard
    bind = op.get_bind()
    inspector = inspect(bind)

    # organizations depends only on itself
    if not inspector.has_table("organizations"):
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

    # organization_members depends on users + organizations
    inspector = inspect(bind)  # refresh view
    if not inspector.has_table("organization_members"):
        if not inspector.has_table("organizations"):
            return
        if not inspector.has_table("users"):
            return

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
    bind = op.get_bind()
    inspector = inspect(bind)

    if inspector.has_table("organization_members"):
        op.drop_table("organization_members")

    inspector = inspect(bind)
    if inspector.has_table("organizations"):
        op.drop_table("organizations")

