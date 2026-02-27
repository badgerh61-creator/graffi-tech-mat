from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.simulation import (
    SimulationJobCreateRequest,
    SimulationJobCreateResponse,
    SimulationJobStatusResponse,
    TelemetryArtifactResponse,
)
from app.services.simulation_service import create_job_and_run_sync, get_job, get_artifact

router = APIRouter(prefix="/simulation", tags=["simulation"])

def _resolve_snapshot_model():
    # adapt to your repo naming (RenderedSnapshot vs Snapshot)
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot  # type: ignore
        return Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore
        return Snapshot

@router.post("/jobs", response_model=SimulationJobCreateResponse)
def create_sim_job(
    body: SimulationJobCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    Snapshot = _resolve_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == body.snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    # optional access hook if you already have it
    try:
        from app import crud
        fn = getattr(crud, "get_snapshot_if_accessible", None)
        if fn is not None:
            ok = fn(db, snapshot_id=body.snapshot_id, user_id=user.id)
            if not ok:
                raise HTTPException(403, "No access to snapshot")
    except HTTPException:
        raise
    except Exception:
        pass

    job = create_job_and_run_sync(
        db=db,
        snapshot_id=body.snapshot_id,
        scenario=body.scenario.dict(),
        engine_version=body.engine_version,
    )

    return SimulationJobCreateResponse(job_id=job.id, status=job.status, artifact_id=job.artifact_id)

@router.get("/jobs/{job_id}", response_model=SimulationJobStatusResponse)
def get_sim_job(
    job_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    job = get_job(db, job_id)
    if not job:
        raise HTTPException(404, "Job not found")

    return SimulationJobStatusResponse(
        job_id=job.id,
        snapshot_id=job.snapshot_id,
        status=job.status,
        artifact_id=job.artifact_id,
        error=job.error,
    )

@router.get("/artifacts/{artifact_id}", response_model=TelemetryArtifactResponse)
def get_telemetry_artifact(
    artifact_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    art = get_artifact(db, artifact_id)
    if not art:
        raise HTTPException(404, "Artifact not found")

    curves = json.loads(art.curves_json or "{}")
    return TelemetryArtifactResponse(
        artifact_id=art.id,
        snapshot_id=art.snapshot_id,
        engine_version=art.engine_version,
        timestep_s=float(art.timestep_ms) / 1000.0,
        duration_s=float(art.duration_s),
        curves=curves,
    )
