from __future__ import annotations

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base


class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True, nullable=False)

    name = Column(String(120), nullable=False)
    scenario_json = Column(Text, nullable=False)

    # 6S.6 (additive): template + reproducibility metadata
    template_key = Column(String(64), nullable=True)
    template_version = Column(String(16), nullable=True)
    engine_version = Column(String(64), nullable=False, default="pseudo-v1")
    scenario_hash = Column(String(128), nullable=False, index=True, default="")

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
