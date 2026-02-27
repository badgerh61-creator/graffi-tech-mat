from __future__ import annotations

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db

from app.schemas.simulation_lab import (
    ScenarioCreateRequest, ScenarioCreateResponse,
    ScenarioListResponse, ScenarioListItem,
    RunCreateRequest, RunCreateResponse,
    RunListResponse, RunListItem,
    CompareMatrixRequest, CompareMatrixResponse,
)

from app.services.simulation_scenarios import create_scenario, list_scenarios, get_scenario
from app.services.simulation_runs import create_run_index, list_runs
from app.services.telemetry_compare_matrix import build_compare_matrix
from app.services.simulation_service import create_job_and_run_sync

# Tier 6S.9 hashing helpers (best-effort, safe)
try:
    from app.services.reproducibility import stable_hash as _stable_hash
except Exception:  # pragma: no cover
    _stable_hash = None

try:
    from app.services.scenario_hashing import compute_scenario_hash as _compute_scenario_hash
except Exception:  # pragma: no cover
    _compute_scenario_hash = None


router = APIRouter(prefix="/simulation", tags=["simulation-lab"])


@router.post("/scenarios", response_model=ScenarioCreateResponse)
def create_scenario_endpoint(
    body: ScenarioCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    out = create_scenario(
        db=db,
        project_id=body.project_id,
        name=body.name,
        scenario=body.scenario,
        user_id=user.id,
    )

    # Backward compatible: create_scenario may return int OR dict depending on your tier version.
    if isinstance(out, dict):
        sid = out.get("scenario_id")
    else:
        sid = out

    return ScenarioCreateResponse(scenario_id=int(sid))


@router.get("/scenarios", response_model=ScenarioListResponse)
def list_scenarios_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    scenarios = list_scenarios(db=db, project_id=project_id)
    return ScenarioListResponse(
        project_id=project_id,
        scenarios=[ScenarioListItem(**s) for s in scenarios],
    )


def _resolve_snapshot_model():
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot  # type: ignore
        return Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore
        return Snapshot


def _compute_snapshot_hash_best_effort(snap) -> str:
    """
    Best-effort deterministic hash. Never assumes fields exist.
    If hashing helper missing, returns "" (safe).
    """
    if not _stable_hash:
        return ""
    payload = {
        "id": int(getattr(snap, "id", 0) or 0),
        "updated_at": str(getattr(snap, "updated_at", "") or ""),
        "scene_json": str(getattr(snap, "scene_json", "") or ""),
        "state_json": str(getattr(snap, "state_json", "") or ""),
        "content_json": str(getattr(snap, "content_json", "") or ""),
        "metrics_json": str(getattr(snap, "metrics_json", "") or ""),
    }
    return _stable_hash(payload)


def _compute_scenario_hash_best_effort(*, scenario: dict, engine_version: str) -> str:
    """
    If scenario hashing helper exists (6S.6), use it. Otherwise return "" (safe).
    """
    if not _compute_scenario_hash:
        return ""
    return _compute_scenario_hash(
        scenario=scenario or {},
        template_key=None,
        template_version=None,
        engine_version=engine_version,
    )


@router.post("/run", response_model=RunCreateResponse)
def run_scenario_endpoint(
    body: RunCreateRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # enforce exactly one of scenario_id or scenario
    if (body.scenario_id is None and body.scenario is None) or (
        body.scenario_id is not None and body.scenario is not None
    ):
        raise HTTPException(422, "Provide exactly one of scenario_id or scenario")

    Snapshot = _resolve_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == body.snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    project_id = int(getattr(snap, "project_id", 0))
    if project_id <= 0:
        raise HTTPException(422, "Snapshot missing project_id")

    scenario_id = body.scenario_id
    scenario = body.scenario

    if scenario_id is not None:
        s = get_scenario(db=db, scenario_id=int(scenario_id))
        scenario = s["scenario"]

    # Create artifact using the same path as 6S.1 (job + artifact)
    job = create_job_and_run_sync(
        db=db,
        snapshot_id=int(body.snapshot_id),
        scenario=scenario or {},
        engine_version=body.engine_version,
    )
    if not job.artifact_id:
        raise HTTPException(500, "simulation did not produce artifact")

    # Tier 6S.9: compute hashes (safe if helpers missing)
    snapshot_hash = _compute_snapshot_hash_best_effort(snap)
    scenario_hash = _compute_scenario_hash_best_effort(scenario=scenario or {}, engine_version=body.engine_version)

    run_id = create_run_index(
        db=db,
        project_id=project_id,
        snapshot_id=int(body.snapshot_id),
        scenario_id=int(scenario_id) if scenario_id is not None else None,
        artifact_id=int(job.artifact_id),
        engine_version=body.engine_version,
        user_id=user.id,

        # optional, backward compatible
        snapshot_hash=snapshot_hash,
        scenario_hash=scenario_hash,
    )

    return RunCreateResponse(run_id=run_id, artifact_id=int(job.artifact_id))


@router.get("/runs", response_model=RunListResponse)
def list_runs_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    runs = list_runs(db=db, project_id=project_id)
    return RunListResponse(
        project_id=project_id,
        runs=[RunListItem(**r) for r in runs],
    )


@router.post("/compare/matrix", response_model=CompareMatrixResponse)
def compare_matrix_endpoint(
    body: CompareMatrixRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # fetch artifacts via existing TelemetryArtifact model
    from app.models.telemetry_artifact import TelemetryArtifact

    rows = db.query(TelemetryArtifact).filter(TelemetryArtifact.id.in_(body.artifact_ids)).all()
    if len(rows) != len(set(body.artifact_ids)):
        raise HTTPException(404, "One or more artifacts not found")

    artifacts = []
    for r in rows:
        # compatibility: some tiers used timestep_s (ms int), some may have timestep_ms
        timestep_ms = getattr(r, "timestep_s", None)
        if timestep_ms is None:
            timestep_ms = getattr(r, "timestep_ms", None)
        if timestep_ms is None:
            timestep_ms = 100  # safe fallback (0.1s)

        artifacts.append(
            {
                "id": int(r.id),
                "curves": json.loads(r.curves_json or "{}"),
                "timestep_s": float(timestep_ms) / 1000.0,
                "duration_s": float(getattr(r, "duration_s", 0.0) or 0.0),
            }
        )

    matrix = build_compare_matrix(artifacts=artifacts)
    ids = sorted(list(set(body.artifact_ids)))
    return CompareMatrixResponse(artifact_ids=ids, matrix=matrix)
