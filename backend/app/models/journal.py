from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)

    type = Column(String, nullable=False, index=True)

    # Phase I.7: scene == project
    scene_id = Column(Integer, nullable=False, index=True)

    snapshot_id = Column(
        Integer,
        ForeignKey("rendered_snapshots.id", ondelete="CASCADE"),
        nullable=True,
    )

    actor_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ✅ REQUIRED BY PHASE I.7 AUDIT CONTRACT
    scene_hash = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

