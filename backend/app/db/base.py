from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import ALL model modules so Alembic sees them
from app.models import (  # noqa: F401
    user,
    asset,
    model,
    model_permission,
    audit_log,
    organization,
    organization_member,
)
