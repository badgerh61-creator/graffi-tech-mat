# backend/app/models/model_owner.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from app.db.base import Base


class ModelOwner(Base):
    __tablename__ = "model_owners"

    id = Column(Integer, primary_key=True)

    model_id = Column(
        Integer,
        ForeignKey("models.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    owner_type = Column(
        String,
        nullable=False,  # 'user' | 'organization'
    )

    owner_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )

    owner_org_id = Column(
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "(owner_user_id IS NOT NULL AND owner_org_id IS NULL) OR "
            "(owner_user_id IS NULL AND owner_org_id IS NOT NULL)",
            name="ck_model_owners_exactly_one_owner",
        ),
        CheckConstraint(
            "owner_type IN ('user', 'organization')",
            name="ck_model_owners_owner_type",
        ),
        UniqueConstraint("model_id", name="uq_model_owners_model_id"),
    )

