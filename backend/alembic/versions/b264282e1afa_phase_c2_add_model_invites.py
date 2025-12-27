# backend/alembic/versions/b264282e1afa_phase_c2_add_model_invites.py

from alembic import op
import sqlalchemy as sa

revision = "b264282e1afa"
down_revision = "phase11_add_asset_metadata"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "model_invites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("models.id", ondelete="CASCADE")),
        sa.Column("email", sa.String(255), nullable=False, index=True),
        sa.Column("role", sa.String(20), nullable=False, server_default="viewer"),
        sa.Column("token", sa.String(64), nullable=False, unique=True, index=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table("model_invites")

