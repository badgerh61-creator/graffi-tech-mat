from __future__ import annotations

import json
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.simulation_scenario import SimulationScenario
from app.services.scenario_hashing import compute_scenario_hash


def create_scenario(
    *,
    db: Session,
    project_id: int,
    name: str,
    scenario: dict,
    user_id: int,
    engine_version: str = "pseudo-v1",
    template_key: str | None = None,
    template_version: str | None = None,
) -> dict:
    scenario_obj = scenario or {}

    scenario_hash = compute_scenario_hash(
        scenario=scenario_obj,
        template_key=template_key,
        template_version=template_version,
        engine_version=engine_version,
    )

    row = SimulationScenario(
        project_id=project_id,
        name=name,
        scenario_json=json.dumps(scenario_obj, sort_keys=True),
        created_by=user_id,
        template_key=template_key,
        template_version=template_version,
        engine_version=engine_version,
        scenario_hash=scenario_hash,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {"scenario_id": int(row.id), "scenario_hash": scenario_hash}


def list_scenarios(*, db: Session, project_id: int):
    rows = (
        db.query(SimulationScenario)
        .filter(SimulationScenario.project_id == project_id)
        .order_by(SimulationScenario.id.asc())
        .all()
    )
    return [
        {
            "id": int(r.id),
            "name": r.name,
            "scenario": json.loads(r.scenario_json or "{}"),
            # optional (safe to include; helps lab UI)
            "scenario_hash": getattr(r, "scenario_hash", "") or "",
            "template_key": getattr(r, "template_key", None),
            "template_version": getattr(r, "template_version", None),
            "engine_version": getattr(r, "engine_version", "pseudo-v1"),
        }
        for r in rows
    ]


def get_scenario(*, db: Session, scenario_id: int) -> dict:
    row = db.query(SimulationScenario).filter(SimulationScenario.id == scenario_id).first()
    if not row:
        raise HTTPException(404, "Scenario not found")

    return {
        "id": int(row.id),
        "project_id": int(row.project_id),
        "name": row.name,
        "scenario": json.loads(row.scenario_json or "{}"),
        "scenario_hash": getattr(row, "scenario_hash", "") or "",
        "template_key": getattr(row, "template_key", None),
        "template_version": getattr(row, "template_version", None),
        "engine_version": getattr(row, "engine_version", "pseudo-v1"),
    }
