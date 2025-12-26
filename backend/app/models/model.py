# backend/app/models/model.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ModelRecord(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="models")

    assets = relationship(
        "Asset",
        back_populates="model",
        cascade="all, delete-orphan",
    )

    permissions = relationship(
        "ModelPermission",
        cascade="all, delete-orphan",
    )

    # 🔵 PHASE C2 — email invites
    invites = relationship(
        "ModelInvite",
        cascade="all, delete-orphan",
    )

