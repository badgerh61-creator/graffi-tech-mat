from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "xxxx"
down_revision = None  # keep what Alembic generated
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    columns = [col["name"] for col in inspector.get_columns("models")]

    # Only rename if old column exists and new one does not
    if "metadata" in columns and "model_metadata" not in columns:
        op.alter_column(
            "models",
            "metadata",
            new_column_name="model_metadata",
            existing_type=sa.JSON(),
        )


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    columns = [col["name"] for col in inspector.get_columns("models")]

    if "model_metadata" in columns and "metadata" not in columns:
        op.alter_column(
            "models",
            "model_metadata",
            new_column_name="metadata",
            existing_type=sa.JSON(),
        )
