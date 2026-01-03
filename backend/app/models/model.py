from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class ModelRecord(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # 🆕 Phase I.3 — active preview camera preset (ID only)
    preview_camera_preset_id = Column(
        String,
        nullable=False,
        default="front_iso",
    )

    # 🔴 Legacy owner (DO NOT REMOVE)
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 🔗 LEGACY OWNER
    owner = relationship("User", back_populates="models")

    # 🆕 OWNERSHIP BRIDGE (read-only, optional)
    ownership = relationship(
        "ModelOwner",
        uselist=False,
        viewonly=True,
        primaryjoin="ModelRecord.id == foreign(ModelOwner.model_id)",
    )

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

    # 🔗 PATCH REGISTRY
    patches = relationship(
        "PatchRegistry",
        back_populates="model",
        cascade="all, delete-orphan",
    )

