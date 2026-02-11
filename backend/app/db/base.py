# backend/app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import ALL model modules so Alembic / SQLAlchemy sees them
# IMPORTANT: keep this list explicit and closed
from app.models import (  # noqa: F401
    # Core
    user,
    job,
    asset,
    model,
    model_permission,
    model_invite,
    refresh_token,
    audit_log,

    # Organizations
    organization,
    organization_member,

    # Projects & snapshots
    project,
    rendered_snapshot,

    # Phase E — LEGACY export intent (DISABLED)
    # export,  # ⛔ DO NOT IMPORT (legacy table only)

    # Phase M — export execution ONLY
    export_job,

    # Phase N — distribution
    distribution_request,
    signed_url,

    # Mutations / journaling
    mutation_journal,

    # Infra
    patch_registry,
)

