"""
⚠️ DEPRECATED — PHASE I.7 LEGACY JOURNAL MODEL

This file is intentionally retained for historical reference only.

Status:
- Deprecated as of Phase K
- DO NOT IMPORT
- DO NOT REGISTER WITH SQLAlchemy METADATA
- DO NOT USE IN NEW CODE

Superseded by:
    app.models.journal_entry.JournalEntry

Reason:
- This model represents the old Phase I.7 "scene journal"
- Phase K+ uses project-scoped mutation journaling
- Keeping this active causes ORM table conflicts

This file must remain isolated in app.models.legacy
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.base import Base


class LegacyJournalEntry(Base):
    __tablename__ = "journal_entries"

    # IMPORTANT:
    # This class must NEVER be imported into active metadata.
    # It exists only as a reference snapshot of the old schema.

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

    # Phase I.7 audit field (obsolete)
    scene_hash = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

