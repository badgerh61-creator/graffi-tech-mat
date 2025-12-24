from alembic import op
import sqlalchemy as sa

revision = "<PUT_REVISION_ID_HERE>"
down_revision = "d3fe5f80b9fc"  # audit logs revision
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "assets",
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "assets",
        sa.Column("processing_error", sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_column("assets", "processing_error")
    op.drop_column("assets", "processed_at")

