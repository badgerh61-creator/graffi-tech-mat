from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.simulation_run import SimulationRun


def create_run_index(
    *,
    db: Session,
    project_id: int,
    snapshot_id: int,
    scenario_id: int | None,
    artifact_id: int,
    engine_version: str,
    user_id: int,
) -> int:
    row = SimulationRun(
        project_id=project_id,
        snapshot_id=snapshot_id,
        scenario_id=scenario_id,
        artifact_id=artifact_id,
        engine_version=engine_version,
        created_by=user_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return int(row.id)


def list_runs(*, db: Session, project_id: int):
    rows = (
        db.query(SimulationRun)
        .filter(SimulationRun.project_id == project_id)
        .order_by(SimulationRun.id.asc())
        .all()
    )
    return [
        {
            "run_id": int(r.id),
            "artifact_id": int(r.artifact_id),
            "snapshot_id": int(r.snapshot_id),
            "scenario_id": int(r.scenario_id) if r.scenario_id is not None else None,
            "engine_version": r.engine_version,
        }
        for r in rows
    ]
