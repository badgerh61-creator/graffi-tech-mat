# backend/alembic/versions/e96b97d898c2_f2_4_add_model_owners.py

"""
Phase F2.4 — Model Ownership Bridge

This migration introduces a canonical ownership bridge that allows
a model to be owned by either a user OR an organization.

Design goals:
- No breaking changes
- No polymorphic ORM patterns
- Backward compatibility with user-owned models
- One owner per model
"""

from alembic import op
import sqlalchemy as sa


# Alembic revision identifiers
revision = "e96b97d898c2"
down_revision = "afe3fa68ab1f"
branch_labels = None
depends_on = None


def upgrade():
    # ------------------------------------------------------------------
    # model_owners table
    # ------------------------------------------------------------------
    op.create_table(
        "model_owners",
        sa.Column("id", sa.Integer(), primary_key=True),

        sa.Column(
            "model_id",
            sa.Integer(),
            sa.ForeignKey("models.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),

        sa.Column(
            "owner_type",
            sa.String(length=20),
            nullable=False,  # 'user' | 'organization'
        ),

        sa.Column(
            "owner_user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=True,
        ),

        sa.Column(
            "owner_org_id",
            sa.Integer(),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        # Enforce exactly one owner
        sa.CheckConstraint(
            "(owner_user_id IS NOT NULL AND owner_org_id IS NULL) OR "
            "(owner_user_id IS NULL AND owner_org_id IS NOT NULL)",
            name="ck_model_owners_exactly_one_owner",
        ),
    )


def downgrade():
    op.drop_table("model_owners")

