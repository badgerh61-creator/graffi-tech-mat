from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.base import Base


class InviteStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    revoked = "revoked"


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

    status = Column(
        Enum(InviteStatus, name="invite_status"),
        nullable=False,
        default=InviteStatus.pending,
    )

    invited_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    accepted_at = Column(DateTime(timezone=True), nullable=True)

    # ✅ FIX: explicitly link both sides + silence overlap warning
    model = relationship(
        "ModelRecord",
        back_populates="invites",
        overlaps="invites",
    )

    invited_by = relationship("User")

    __table_args__ = (
        UniqueConstraint("model_id", "email", name="uq_model_invite_email"),
    )

