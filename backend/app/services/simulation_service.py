# backend/app/services/simulation_service.py
from __future__ import annotations

from typing import Any, Dict, Optional
import json
import hashlib

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.simulation_job import SimulationJob
from app.models.telemetry_artifact import TelemetryArtifact
from app.services.simulation_engine_registry import engine_registry


def _stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def create_job_and_run_sync(
    *,
    db: Session,
    snapshot_id: int,
    scenario: Dict[str, Any],
    engine_version: str,
) -> SimulationJob:
    """
    6S.1 baseline: record a job then execute immediately (sync) and store artifact.
    6S.2: execution is routed through the engine registry (plugin slot).
    """
    job = SimulationJob(
        snapshot_id=snapshot_id,
        engine_version=engine_version,
        status="running",
        scenario_json=json.dumps(scenario, sort_keys=True),
        artifact_id=None,
        error=None,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        # 6S.2: resolve engine via registry
        try:
            engine = engine_registry.get(engine_version)
        except ValueError as e:
            # Preserve contract: unknown engine => 422
            raise HTTPException(422, str(e))

        result = engine.run(snapshot_id=snapshot_id, scenario=scenario)

        curves = result.get("curves") or {}
        timestep_s = float(result.get("timestep_s", float(scenario.get("timestep_s", 0.1))))
        duration_s = float(result.get("duration_s", float(scenario.get("duration_s", 10.0))))

        scenario_hash = _stable_hash({"scenario": scenario, "engine_version": engine_version})

        art = TelemetryArtifact(
            snapshot_id=snapshot_id,
            scenario_hash=scenario_hash,
            engine_version=engine_version,
            timestep_ms=int(round(timestep_s * 1000.0)),
            duration_s=int(round(duration_s)),
            curves_json=json.dumps(curves, sort_keys=True),
        )
        db.add(art)
        db.commit()
        db.refresh(art)

        job.status = "succeeded"
        job.artifact_id = art.id
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    except HTTPException as e:
        job.status = "failed"
        job.error = str(e.detail)
        db.add(job)
        db.commit()
        db.refresh(job)
        raise
    except Exception as e:
        job.status = "failed"
        job.error = f"sim failed: {e}"
        db.add(job)
        db.commit()
        db.refresh(job)
        raise HTTPException(500, "simulation failed") from e


def get_job(db: Session, job_id: int) -> Optional[SimulationJob]:
    return db.query(SimulationJob).filter(SimulationJob.id == job_id).first()


def get_artifact(db: Session, artifact_id: int) -> Optional[TelemetryArtifact]:
    return db.query(TelemetryArtifact).filter(TelemetryArtifact.id == artifact_id).first()
