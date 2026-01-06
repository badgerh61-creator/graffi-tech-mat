# backend/app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import ALL model modules so Alembic sees them
# IMPORTANT: keep this list explicit and closed
from app.models import (  # noqa: F401
    user,
    job,
    asset,
    model,
    model_permission,
    model_invite,
    refresh_token,
    audit_log,
    organization,
    organization_member,
    patch_registry,
    project,
    rendered_snapshot,
    mutation_journal,
)

