"""add optional job_id to export intent

Revision ID: 41e584782df1
Revises: 4d4a4ebe64db
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "41e584782df1"
down_revision = "4d4a4ebe64db"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    # ✅ SQLite-safe batch migration
    # ✅ MINIMAL FIX: pass resolve_fks correctly via reflect_kwargs (prevents reflection issues)
    with op.batch_alter_table(
        "exports",
        reflect_kwargs={"resolve_fks": False},
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "job_id",
                sa.String(length=36),
                nullable=True,
            )
        )

        # ✅ MINIMAL GUARD: only create FK if target table exists
        if inspector.has_table("export_jobs"):
            batch_op.create_foreign_key(
                "fk_exports_job_id_export_jobs",
                "export_jobs",
                ["job_id"],
                ["id"],
                ondelete="SET NULL",
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    with op.batch_alter_table(
        "exports",
        reflect_kwargs={"resolve_fks": False},
    ) as batch_op:

        # ✅ MINIMAL GUARD: only drop FK if target table exists
        if inspector.has_table("export_jobs"):
            # If constraint doesn't exist (some DBs), this can throw; keep it safe.
            try:
                batch_op.drop_constraint(
                    "fk_exports_job_id_export_jobs",
                    type_="foreignkey",
                )
            except Exception:
                pass

        batch_op.drop_column("job_id")

