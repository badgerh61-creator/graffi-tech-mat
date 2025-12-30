# backend/app/models/model_invite.py
# =========================================
# Graffi-Tech-Mat — Model Invite (Phase 4.6 FINAL)
# Status-free • Migration-free • SQLite-safe
# =========================================

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ModelInvite(Base):
    __tablename__ = "model_invites"

    id = Column(Integer, primary_key=True)

    model_id = Column(
        Integer,
        ForeignKey("models.id", ondelete="CASCADE"),
        nullable=False,
    )

    email = Column(String, nullable=False, index=True)

    # viewer | editor
    role = Column(String, nullable=False, default="viewer")

    token = Column(String, nullable=False, unique=True, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    model = relationship("ModelRecord", back_populates="invites")

    __table_args__ = (
        UniqueConstraint("model_id", "email", name="uq_model_invite_email"),
    )

