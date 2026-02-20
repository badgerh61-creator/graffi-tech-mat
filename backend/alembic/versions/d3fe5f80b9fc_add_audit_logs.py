from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "d3fe5f80b9fc"
down_revision = "baseline_0001"
branch_labels = None
depends_on = None


def upgrade():
    # ✅ SAFETY: do nothing if the table already exists
    bind = op.get_bind()
    inspector = inspect(bind)
    if "audit_logs" in inspector.get_table_names():
        return

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("resource_type", sa.String(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=True),

        # ❗ renamed column
        sa.Column("extra", sa.JSON(), nullable=True),

        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("user_agent", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade():
    # ✅ SAFETY: only drop if it exists
    bind = op.get_bind()
    inspector = inspect(bind)
    if "audit_logs" not in inspector.get_table_names():
        return

    op.drop_table("audit_logs")

