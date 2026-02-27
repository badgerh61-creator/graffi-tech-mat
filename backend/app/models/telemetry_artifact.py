from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class TelemetryArtifact(Base):
    __tablename__ = "telemetry_artifacts"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, index=True, nullable=False)

    scenario_hash = Column(String(128), nullable=False, index=True)
    engine_version = Column(String(64), nullable=False, default="pseudo-v1")

    timestep_ms = Column(Integer, nullable=False, default=100)  # store ms
    duration_s = Column(Integer, nullable=False, default=10)    # store seconds int

    curves_json = Column(Text, nullable=False, default="{}")

    # 6S.8 (ADD ONLY): optional engine metadata (endurance, model_version, notes, etc.)
    # Default keeps older tiers stable.
    meta_json = Column(Text, nullable=False, default="{}")

    job = relationship("SimulationJob", back_populates="artifact")
