from sqlalchemy import Column, Integer, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class DraftLock(Base):
    __tablename__ = "draft_locks"

    id = Column(Integer, primary_key=True)
    snapshot_id = Column(Integer, nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    acquired_at = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("snapshot_id", name="uq_draft_lock_snapshot"),
    )

