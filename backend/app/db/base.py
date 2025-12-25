# backend/app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ✅ Import ALL current model modules so Alembic sees them
# (module names must match actual filenames)

from app.models import (  # noqa: F401
    user,
    asset,
    model,              # ✅ WAS model_record
    model_permission,
    audit_log,
)

