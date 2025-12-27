# backend/app/models/patch_registry.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class PatchRegistry(Base):
    __tablename__ = "patch_registry"

    id = Column(Integer, primary_key=True, index=True)

    model_id = Column(
        Integer,
        ForeignKey("models.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    patch_name = Column(String, nullable=False)
    patch_version = Column(String, nullable=False)

    # ✅ SAFE name (not metadata)
    patch_metadata = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    model = relationship(
        "ModelRecord",
        back_populates="patches",
    )

