from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base


class SimulationBatch(Base):
    __tablename__ = "simulation_batches"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, index=True, nullable=False)
    snapshot_id = Column(Integer, index=True, nullable=False)
    engine_version = Column(String(64), nullable=False, default="pseudo-v1")

    status = Column(String(16), nullable=False, default="queued")

    scenario_ids_json = Column(Text, nullable=False, default="[]")
    template_keys_json = Column(Text, nullable=False, default="[]")

    run_ids_json = Column(Text, nullable=False, default="[]")
    artifact_ids_json = Column(Text, nullable=False, default="[]")

    error = Column(Text, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
