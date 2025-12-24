# backend/app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


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
        default="viewer",  # viewer | editor | admin
    )

    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

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

