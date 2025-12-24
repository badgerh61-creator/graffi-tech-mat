"""
Baseline schema freeze.

This migration declares the current database schema as canonical.
No schema operations are performed.
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "baseline_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Database schema already exists.
    # This migration intentionally does nothing.
    pass


def downgrade():
    # No downgrade path from baseline.
    pass

