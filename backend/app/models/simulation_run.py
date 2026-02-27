from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, index=True, nullable=False)
    snapshot_id = Column(Integer, index=True, nullable=False)

    scenario_id = Column(Integer, ForeignKey("simulation_scenarios.id"), nullable=True)

    artifact_id = Column(Integer, index=True, nullable=False)
    engine_version = Column(String(64), nullable=False)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
