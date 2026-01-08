from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    mutation_type = Column(String, nullable=False)

    snapshot_before = Column(Integer, nullable=False)
    snapshot_after = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

