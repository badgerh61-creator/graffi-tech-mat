from __future__ import annotations

from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field

JobStatus = Literal["queued", "running", "succeeded", "failed"]

class SimulationScenario(BaseModel):
    duration_s: float = Field(default=10.0, gt=0, le=3600)
    timestep_s: float = Field(default=0.1, gt=0, le=10)
    throttle: float = Field(default=0.6, ge=0.0, le=1.0)
    gear_ratio: float = Field(default=10.0, gt=0, le=1000)
    mass_kg: float = Field(default=1200.0, gt=1, le=100000)

class SimulationJobCreateRequest(BaseModel):
    snapshot_id: int
    scenario: SimulationScenario = Field(default_factory=SimulationScenario)
    engine_version: str = Field(default="pseudo-v1", min_length=1)

class SimulationJobCreateResponse(BaseModel):
    job_id: int
    status: JobStatus
    artifact_id: Optional[int] = None

class SimulationJobStatusResponse(BaseModel):
    job_id: int
    snapshot_id: int
    status: JobStatus
    artifact_id: Optional[int] = None
    error: Optional[str] = None

class TelemetryArtifactResponse(BaseModel):
    artifact_id: int
    snapshot_id: int
    engine_version: str
    timestep_s: float
    duration_s: float
    curves: Dict[str, Any]
