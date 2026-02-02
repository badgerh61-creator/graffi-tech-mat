from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime

from app.db.base import Base


class ReadView(Base):
    __tablename__ = "read_views"

    id = Column(Integer, primary_key=True)

    snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id"),
        nullable=False,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    session_id = Column(
        Integer,
        ForeignKey("presence_sessions.id"),
        nullable=False,
        index=True,
    )

    opened_at = Column(DateTime, nullable=False, default=datetime.utcnow)

