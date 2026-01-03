# backend/app/models/mutation_journal.py

from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func

from app.db.base import Base


class MutationJournal(Base):
    __tablename__ = "mutation_journal"

    id = Column(Integer, primary_key=True, index=True)

    intent_type = Column(String, nullable=False)          # e.g. RenameAsset
    target_type = Column(String, nullable=False)          # e.g. asset
    target_id = Column(Integer, nullable=False)

    before_state = Column(JSON, nullable=False)
    after_state = Column(JSON, nullable=False)

    issued_by_user_id = Column(Integer, nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())

    reason = Column(String, nullable=True)

