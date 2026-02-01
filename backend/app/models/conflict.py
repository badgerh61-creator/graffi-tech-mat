from sqlalchemy import Column, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class SnapshotConflict(Base):
    __tablename__ = "snapshot_conflicts"

    id = Column(Integer, primary_key=True)

    snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    detected_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    reason = Column(Text, nullable=False)

