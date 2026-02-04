"""add optional job_id to export intent

Revision ID: 41e584782df1
Revises: 4d4a4ebe64db
"""

from alembic import op
import sqlalchemy as sa

revision = "41e584782df1"
down_revision = "4d4a4ebe64db"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLite-safe batch migration
    with op.batch_alter_table("exports") as batch_op:
        batch_op.add_column(
            sa.Column(
                "job_id",
                sa.String(length=36),
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "fk_exports_job_id_export_jobs",
            "export_jobs",
            ["job_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("exports") as batch_op:
        batch_op.drop_constraint(
            "fk_exports_job_id_export_jobs",
            type_="foreignkey",
        )
        batch_op.drop_column("job_id")

