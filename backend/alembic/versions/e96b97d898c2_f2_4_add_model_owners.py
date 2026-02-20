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
from sqlalchemy import inspect  # ✅ minimal add


# Alembic revision identifiers
revision = "e96b97d898c2"
down_revision = "afe3fa68ab1f"
branch_labels = None
depends_on = None


def upgrade():
    # ✅ minimal add: idempotent + guard prerequisite tables
    bind = op.get_bind()
    inspector = inspect(bind)

    # If the bridge table already exists, skip safely
    if inspector.has_table("model_owners"):
        return

    # If core prereqs aren't present yet, skip (prevents "no such table" issues)
    if not inspector.has_table("models"):
        return
    if not inspector.has_table("users"):
        return
    if not inspector.has_table("organizations"):
        return

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
    # ✅ minimal add: safe drop
    bind = op.get_bind()
    inspector = inspect(bind)
    if not inspector.has_table("model_owners"):
        return

    op.drop_table("model_owners")

