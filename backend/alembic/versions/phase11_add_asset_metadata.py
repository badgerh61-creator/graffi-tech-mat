# backend/alembic/versions/phase11_add_asset_metadata.py

"""
Phase 11 — asset metadata & thumbnails (NO-OP RECOVERY)

Recreated to repair Alembic revision graph.
Schema already exists in database.
"""

from alembic import op
import sqlalchemy as sa

revision = "phase11_add_asset_metadata"
down_revision = "1013228e1acd"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass

