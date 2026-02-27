from __future__ import annotations

from typing import Any, Dict, Optional
import json, hashlib
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.simulation_job import SimulationJob
from app.models.telemetry_artifact import TelemetryArtifact
from app.services.pseudo_sim_engine import PseudoSimScenario, run_pseudo_sim

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
    # 6S.1 baseline: record a job, run immediately, store artifact
    job = SimulationJob(
        snapshot_id=snapshot_id,
        engine_version=engine_version,
        status="running",
        scenario_json=json.dumps(scenario, sort_keys=True),
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        if engine_version != "pseudo-v1":
            raise HTTPException(422, "unknown engine_version")

        sc = PseudoSimScenario(
            duration_s=float(scenario.get("duration_s", 10.0)),
            timestep_s=float(scenario.get("timestep_s", 0.1)),
            throttle=float(scenario.get("throttle", 0.6)),
            gear_ratio=float(scenario.get("gear_ratio", 10.0)),
            mass_kg=float(scenario.get("mass_kg", 1200.0)),
        )

        curves = run_pseudo_sim(scenario=sc)

        scenario_hash = _stable_hash({"scenario": scenario, "engine_version": engine_version})

        art = TelemetryArtifact(
            snapshot_id=snapshot_id,
            scenario_hash=scenario_hash,
            engine_version=engine_version,
            timestep_ms=int(round(sc.timestep_s * 1000.0)),
            duration_s=int(round(sc.duration_s)),
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
