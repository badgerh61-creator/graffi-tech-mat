from __future__ import annotations

from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class SimulationJob(Base):
    __tablename__ = "simulation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, index=True, nullable=False)

    engine_version = Column(String(64), nullable=False, default="pseudo-v1", index=True)
    status = Column(String(16), nullable=False, default="queued", index=True)

    scenario_json = Column(Text, nullable=False, default="{}")

    artifact_id = Column(Integer, ForeignKey("telemetry_artifacts.id"), nullable=True)
    error = Column(Text, nullable=True)

    # 6S future-proof (ADD ONLY): timestamps help async + debugging
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # one-to-one link
    artifact = relationship("TelemetryArtifact", back_populates="job", uselist=False)
