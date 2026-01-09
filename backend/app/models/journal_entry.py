from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    # IMPORTANT: reuse existing table safely
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)

    # --------------------------------------------------
    # 🔁 LEGACY COLUMNS (MUST EXIST + MUST BE FILLED)
    # --------------------------------------------------
    type = Column(String, nullable=False)
    scene_id = Column(Integer, nullable=True)
    snapshot_id = Column(Integer, nullable=True)
    actor_user_id = Column(Integer, nullable=True)
    scene_hash = Column(String, nullable=True)

    # --------------------------------------------------
    # ✅ PHASE I / K CANONICAL COLUMNS
    # --------------------------------------------------
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    mutation_type = Column(String, nullable=False, index=True)

    snapshot_before = Column(Integer, nullable=False)
    snapshot_after = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

