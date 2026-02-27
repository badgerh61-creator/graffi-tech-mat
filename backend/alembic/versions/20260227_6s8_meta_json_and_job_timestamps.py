"""Tier 6S.8: telemetry meta_json + simulation job timestamps

Revision ID: 7b1f6b9c2a11
Revises: 41e584782df1
Create Date: 2026-02-27
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision = "7b1f6b9c2a11"
down_revision = "41e584782df1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    # ----------------------------
    # telemetry_artifacts: meta_json (ADD ONLY)
    # ----------------------------
    if inspector.has_table("telemetry_artifacts"):
        cols = {c["name"] for c in inspector.get_columns("telemetry_artifacts")}
        if "meta_json" not in cols:
            with op.batch_alter_table(
                "telemetry_artifacts",
                reflect_kwargs={"resolve_fks": False},
            ) as batch_op:
                batch_op.add_column(
                    sa.Column("meta_json", sa.Text(), nullable=False, server_default="{}")
                )

    # ----------------------------
    # simulation_jobs: created_at / updated_at (ADD ONLY)
    # ----------------------------
    if inspector.has_table("simulation_jobs"):
        cols = {c["name"] for c in inspector.get_columns("simulation_jobs")}
        with op.batch_alter_table(
            "simulation_jobs",
            reflect_kwargs={"resolve_fks": False},
        ) as batch_op:
            if "created_at" not in cols:
                batch_op.add_column(
                    sa.Column(
                        "created_at",
                        sa.DateTime(timezone=True),
                        nullable=False,
                        server_default=sa.func.now(),
                    )
                )
            if "updated_at" not in cols:
                batch_op.add_column(
                    sa.Column(
                        "updated_at",
                        sa.DateTime(timezone=True),
                        nullable=False,
                        server_default=sa.func.now(),
                    )
                )

        # indexes (safe guards)
        existing_indexes = {ix.get("name") for ix in inspector.get_indexes("simulation_jobs")}
        if "ix_simulation_jobs_status" not in existing_indexes:
            op.create_index("ix_simulation_jobs_status", "simulation_jobs", ["status"])
        if "ix_simulation_jobs_engine_version" not in existing_indexes:
            op.create_index("ix_simulation_jobs_engine_version", "simulation_jobs", ["engine_version"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    # Drop indexes if they exist
    if inspector.has_table("simulation_jobs"):
        existing_indexes = {ix.get("name") for ix in inspector.get_indexes("simulation_jobs")}
        if "ix_simulation_jobs_engine_version" in existing_indexes:
            op.drop_index("ix_simulation_jobs_engine_version", table_name="simulation_jobs")
        if "ix_simulation_jobs_status" in existing_indexes:
            op.drop_index("ix_simulation_jobs_status", table_name="simulation_jobs")

        cols = {c["name"] for c in inspector.get_columns("simulation_jobs")}
        with op.batch_alter_table(
            "simulation_jobs",
            reflect_kwargs={"resolve_fks": False},
        ) as batch_op:
            if "updated_at" in cols:
                batch_op.drop_column("updated_at")
            if "created_at" in cols:
                batch_op.drop_column("created_at")

    # Drop meta_json if it exists
    if inspector.has_table("telemetry_artifacts"):
        cols = {c["name"] for c in inspector.get_columns("telemetry_artifacts")}
        with op.batch_alter_table(
            "telemetry_artifacts",
            reflect_kwargs={"resolve_fks": False},
        ) as batch_op:
            if "meta_json" in cols:
                batch_op.drop_column("meta_json")
