from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.services.testing_scenarios_catalog import get_scenario
from app.services.testing_compare_service import compare_snapshots
from app.models.rendered_snapshot import RenderedSnapshot as Snapshot

router = APIRouter(prefix="/testing", tags=["testing"])

@router.get("/compare")
def compare(
    snapshot_a: int = Query(...),
    snapshot_b: int = Query(...),
    scenario_id: str = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    a = db.query(Snapshot).get(snapshot_a)
    b = db.query(Snapshot).get(snapshot_b)

    if not a or not b:
        raise HTTPException(404, "Snapshot not found")

    vehicle_a = {"mass_kg": getattr(a, "vehicle_mass_kg", None)}
    vehicle_b = {"mass_kg": getattr(b, "vehicle_mass_kg", None)}

    out = compare_snapshots(snapshot_a=a, snapshot_b=b, vehicle_a=vehicle_a, vehicle_b=vehicle_b)
    out["scenario"] = scenario
    return out
