"""add jobs table

Revision ID: a39a193688f7
Revises: e2c4a4c776ee
Create Date: 2026-01-03 23:53:13.660594
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a39a193688f7"
down_revision = "e2c4a4c776ee"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mutation_id", sa.Integer(), nullable=False),
        sa.Column("job_type", sa.String(), nullable=False),
        sa.Column("target_type", sa.String(), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column(
            "state",
            sa.Enum(
                "CREATED",
                "RUNNING",
                "COMPLETED",
                "FAILED",
                "CANCELED",
                name="job_state",
            ),
            nullable=False,
            server_default="CREATED",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    # Drop table first
    op.drop_table("jobs")

    # IMPORTANT:
    # SQLite does NOT support DROP TYPE.
    # Only drop enum explicitly on databases that support it.
    bind = op.get_bind()
    if bind.dialect.name != "sqlite":
        op.execute("DROP TYPE job_state")

