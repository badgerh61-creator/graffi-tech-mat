
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import ALL model modules so Alembic sees them
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
)

