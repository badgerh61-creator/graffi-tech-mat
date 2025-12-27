# backend/app/models/model.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


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

    # 🔗 OWNER
    owner = relationship("User", back_populates="models")

    # 🔗 ASSETS
    assets = relationship(
        "Asset",
        back_populates="model",
        cascade="all, delete-orphan",
    )

    # 🔗 PERMISSIONS
    permissions = relationship(
        "ModelPermission",
        back_populates="model",
        cascade="all, delete-orphan",
    )

    # 🔗 EMAIL INVITES (Phase C2)
    invites = relationship(
        "ModelInvite",
        back_populates="model",
        cascade="all, delete-orphan",
    )

    # 🔗 PATCH REGISTRY (FIX for mapper crash)
    patches = relationship(
        "PatchRegistry",
        back_populates="model",
        cascade="all, delete-orphan",
    )

