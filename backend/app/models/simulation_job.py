from __future__ import annotations

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class SimulationJob(Base):
    __tablename__ = "simulation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, index=True, nullable=False)

    engine_version = Column(String(64), nullable=False, default="pseudo-v1")
    status = Column(String(16), nullable=False, default="queued")

    scenario_json = Column(Text, nullable=False, default="{}")

    artifact_id = Column(Integer, ForeignKey("telemetry_artifacts.id"), nullable=True)
    error = Column(Text, nullable=True)

    artifact = relationship("TelemetryArtifact", back_populates="job", uselist=False)
