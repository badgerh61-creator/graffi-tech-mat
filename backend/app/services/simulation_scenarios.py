from __future__ import annotations

import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.simulation_scenario import SimulationScenario


def create_scenario(*, db: Session, project_id: int, name: str, scenario: dict, user_id: int) -> int:
    row = SimulationScenario(
        project_id=project_id,
        name=name,
        scenario_json=json.dumps(scenario or {}, sort_keys=True),
        created_by=user_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return int(row.id)


def list_scenarios(*, db: Session, project_id: int):
    rows = (
        db.query(SimulationScenario)
        .filter(SimulationScenario.project_id == project_id)
        .order_by(SimulationScenario.id.asc())
        .all()
    )
    return [
        {"id": int(r.id), "name": r.name, "scenario": json.loads(r.scenario_json or "{}")}
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
    }
