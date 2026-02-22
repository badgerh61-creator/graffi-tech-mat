from __future__ import annotations

from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class TestingResult(Base):
    __tablename__ = "testing_results"

    id = Column(Integer, primary_key=True, index=True)

    snapshot_id = Column(Integer, nullable=False, index=True)
    scenario_id = Column(String, nullable=False, index=True)

    # Tier 4.4 metrics snapshot (pure output captured at run time)
    metrics = Column(JSON, nullable=False)

    # Optional stable text summary + optional deltas vs baseline
    summary = Column(String, nullable=True)
    deltas = Column(JSON, nullable=True)

    # Job tracking (if you have an AsyncJob table, store its id)
    job_id = Column(String, nullable=True)

    created_by_user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
