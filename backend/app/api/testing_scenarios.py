from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.services.testing_scenarios_catalog import list_scenarios, get_scenario

router = APIRouter(prefix="/testing", tags=["testing"])

@router.get("/scenarios")
def scenarios_list(user=Depends(get_current_user)):
    # Viewer-safe; capability gating can be added if you want, but not required.
    return list_scenarios()

@router.get("/scenarios/{scenario_id}")
def scenarios_detail(scenario_id: str, user=Depends(get_current_user)):
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")
    return scenario
