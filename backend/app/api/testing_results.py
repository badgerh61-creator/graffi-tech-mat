from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.audit import log_event
from app.services.testing_results_service import enqueue_testing_run, get_result
from app.services.testing_scenarios_catalog import get_scenario
from app.models.rendered_snapshot import RenderedSnapshot as Snapshot

router = APIRouter(tags=["testing"])

@router.post("/snapshots/{snapshot_id}/testing/run")
def run_testing(
    snapshot_id: int,
    body: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    scenario_id = (body or {}).get("scenario_id")
    if not scenario_id:
        raise HTTPException(422, "scenario_id required")

    # Snapshot exists check (read-only)
    snapshot = db.query(Snapshot).get(snapshot_id)
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if not get_scenario(scenario_id):
        raise HTTPException(404, "Scenario not found")

    # Recommended policy: allow editor+ only to run jobs.
    # Viewer can still read results.
    # (If you already have capability gating, enforce it here.)
    job_id = enqueue_testing_run(db=db, snapshot=snapshot, user_id=user.id, scenario_id=scenario_id)

    log_event(
        db=db,
        user_id=user.id,
        action="testing.run.requested",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={"scenario_id": scenario_id, "job_id": job_id},
    )

    return {"job_id": job_id}

@router.get("/testing/results/{result_id}")
def read_testing_result(
    result_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    result = get_result(db=db, result_id=result_id)
    if not result:
        raise HTTPException(404, "Result not found")

    return {
        "result_id": result.id,
        "snapshot_id": result.snapshot_id,
        "scenario_id": result.scenario_id,
        "metrics": result.metrics,
        "summary": result.summary,
        "deltas": result.deltas,
        "job_id": result.job_id,
        "created_at": result.created_at.isoformat() if result.created_at else None,
    }
