from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from fastapi.responses import PlainTextResponse
from app.schemas.simulation import (
    SimulationJobCreateRequest,
    SimulationJobCreateResponse,
    SimulationJobStatusResponse,
    TelemetryArtifactResponse,
    TelemetrySummaryResponse,
    TelemetryCompareRequest,
    TelemetryCompareResponse,
)
from app.services.simulation_service import create_job_and_run_sync, get_job, get_artifact
from app.services.telemetry_reports import compute_summary, compute_delta, export_csv

router = APIRouter(prefix="/simulation", tags=["simulation"])

def _resolve_snapshot_model():
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

    # 6S.8 (ADD ONLY): meta if present
    meta = None
    if hasattr(art, "meta_json"):
        try:
            meta = json.loads(getattr(art, "meta_json") or "{}")
        except Exception:
            meta = {}

    return TelemetryArtifactResponse(
        artifact_id=art.id,
        snapshot_id=art.snapshot_id,
        engine_version=art.engine_version,
        timestep_s=float(art.timestep_ms) / 1000.0,
        duration_s=float(art.duration_s),
        curves=curves,
        meta=meta,
    )


# --- Tier 6S.4 (ADD ONLY): summary + compare + CSV export ---

@router.get("/artifacts/{artifact_id}/summary", response_model=TelemetrySummaryResponse)
def artifact_summary(
    artifact_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    art = get_artifact(db, artifact_id)
    if not art:
        raise HTTPException(404, "Artifact not found")

    curves = json.loads(art.curves_json or "{}")
    timestep_s = float(art.timestep_ms) / 1000.0
    duration_s = float(art.duration_s)

    summary = compute_summary(curves=curves, timestep_s=timestep_s, duration_s=duration_s)

    return TelemetrySummaryResponse(
        artifact_id=art.id,
        snapshot_id=art.snapshot_id,
        engine_version=art.engine_version,
        summary=summary,
    )

@router.post("/compare", response_model=TelemetryCompareResponse)
def compare_artifacts(
    body: TelemetryCompareRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    a = get_artifact(db, body.a_artifact_id)
    b = get_artifact(db, body.b_artifact_id)
    if not a or not b:
        raise HTTPException(404, "Artifact not found")

    a_curves = json.loads(a.curves_json or "{}")
    b_curves = json.loads(b.curves_json or "{}")

    a_sum = compute_summary(
        curves=a_curves,
        timestep_s=float(a.timestep_ms) / 1000.0,
        duration_s=float(a.duration_s),
    )
    b_sum = compute_summary(
        curves=b_curves,
        timestep_s=float(b.timestep_ms) / 1000.0,
        duration_s=float(b.duration_s),
    )

    return TelemetryCompareResponse(
        a_artifact_id=a.id,
        b_artifact_id=b.id,
        delta=compute_delta(a_summary=a_sum, b_summary=b_sum),
    )

@router.get("/artifacts/{artifact_id}/export.csv", response_class=PlainTextResponse)
def artifact_export_csv(
    artifact_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    art = get_artifact(db, artifact_id)
    if not art:
        raise HTTPException(404, "Artifact not found")

    curves = json.loads(art.curves_json or "{}")
    csv = export_csv(curves=curves)

    return PlainTextResponse(content=csv, media_type="text/csv")
