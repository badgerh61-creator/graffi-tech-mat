from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class StudioPresence(Base):
    """
    Phase U.1 — Explicit studio presence.
    Presence ≠ permission.
    """

    __tablename__ = "studio_presence"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, nullable=False, index=True)
    project_id = Column(Integer, nullable=False, index=True)

    joined_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

