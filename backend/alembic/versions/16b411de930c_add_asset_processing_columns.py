from alembic import op
import sqlalchemy as sa

# =============================
# Alembic revision identifiers
# =============================

revision = "16b411de930c"
down_revision = "d3fe5f80b9fc"  # audit logs revision
branch_labels = None
depends_on = None


def upgrade():
    # Add processing timestamp
    op.add_column(
        "assets",
        sa.Column(
            "processed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # Add processing error field
    op.add_column(
        "assets",
        sa.Column(
            "processing_error",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("assets", "processing_error")
    op.drop_column("assets", "processed_at")

