# backend/app/api/simulation_repro.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.simulation_run import SimulationRun

router = APIRouter(prefix="/simulation", tags=["simulation-repro"])


@router.get("/runs/{run_id}/repro")
def get_run_repro(
    run_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    r = db.query(SimulationRun).filter(SimulationRun.id == run_id).first()
    if not r:
        raise HTTPException(404, "Run not found")

    # Backward-safe: if old rows exist with null/empty fields, return empty strings / false.
    return {
        "run_id": int(r.id),
        "artifact_id": int(r.artifact_id),
        "snapshot_id": int(r.snapshot_id),
        "scenario_id": int(r.scenario_id) if r.scenario_id is not None else None,
        "engine_version": str(r.engine_version),

        "snapshot_hash": str(getattr(r, "snapshot_hash", "") or ""),
        "scenario_hash": str(getattr(r, "scenario_hash", "") or ""),
        "run_fingerprint": str(getattr(r, "run_fingerprint", "") or ""),
        "verified_deterministic": bool(getattr(r, "verified_deterministic", False)),
    }
