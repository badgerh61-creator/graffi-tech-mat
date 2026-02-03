# backend/app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

from fastapi import Query

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password = Column(String, nullable=False)

    # 🔐 ROLE SYSTEM
    role = Column(
        String,
        nullable=False,
        default="viewer",  # viewer | editor | owner | admin
    )

    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    # ✅ Phase K — per-user capability overrides
    can_tune = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    models = relationship(
        "ModelRecord",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    # -------- ROLE HELPERS --------
    @property
    def is_editor(self) -> bool:
        return self.role in ("editor", "admin")

    @property
    def is_viewer(self) -> bool:
        return self.role in ("viewer", "editor", "admin")


# =====================================================
# Phase E.1 — Studio Read-Only State (NON-PERSISTENT)
# =====================================================
# These are read-only compatibility accessors.
# They do NOT introduce authority.
# They do NOT mutate state.
# They will be overridden by Phase T bindings later.
# =====================================================

@property
def current_station(self) -> str:
    """
    Phase E.1 read-only accessor.

    Station authority lives in the Studio Kernel (Phase T).
    Until bound, return a safe, explicit default.
    """
    return "unknown"


@property
def current_mode(self) -> str:
    """
    Phase E.1 read-only accessor.

    Safe default is read-only.
    """
    return "read_only"


# 🔒 Bind to User model (non-persistent)
User.current_station = current_station
User.current_mode = current_mode

