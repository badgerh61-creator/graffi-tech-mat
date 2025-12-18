from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all model modules so they are registered with Base.metadata
from app.models import (
    user,
    asset,
    model_record,
    model_legacy,
    patch_registry,
)  # noqa: F401

