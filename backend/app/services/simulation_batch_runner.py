from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.simulation_batch import SimulationBatch
from app.services.simulation_scenarios import get_scenario
from app.services.simulation_runs import create_run_index
from app.services.scenario_templates import materialize_template
from app.services.simulation_service import create_job_and_run_sync  # rename if yours differs


def _resolve_snapshot_model():
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot  # type: ignore
        return Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore
        return Snapshot


def create_batch_and_run(
    *,
    db: Session,
    snapshot_id: int,
    engine_version: str,
    scenario_ids: Optional[List[int]],
    template_keys: Optional[List[str]],
    template_overrides: Optional[Dict[str, Dict[str, Any]]],
    user_id: int,
) -> SimulationBatch:
    scenario_ids = sorted(list({int(x) for x in (scenario_ids or [])}))
    template_keys = sorted(list({str(x) for x in (template_keys or [])}))

    if not scenario_ids and not template_keys:
        raise HTTPException(422, "Provide at least one of scenario_ids or template_keys")

    Snapshot = _resolve_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    project_id = int(getattr(snap, "project_id", 0))
    if project_id <= 0:
        raise HTTPException(422, "Snapshot missing project_id")

    batch = SimulationBatch(
        project_id=project_id,
        snapshot_id=snapshot_id,
        engine_version=engine_version,
        status="running",
        scenario_ids_json=json.dumps(scenario_ids),
        template_keys_json=json.dumps(template_keys),
        run_ids_json="[]",
        artifact_ids_json="[]",
        error=None,
        created_by=user_id,
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)

    run_ids: List[int] = []
    artifact_ids: List[int] = []

    try:
        # 1) run saved scenarios
        for sid in scenario_ids:
            s = get_scenario(db=db, scenario_id=sid)
            scenario = s["scenario"]

            job = create_job_and_run_sync(
                db=db,
                snapshot_id=snapshot_id,
                scenario=scenario,
                engine_version=engine_version,
            )
            if not job.artifact_id:
                raise HTTPException(500, "simulation did not produce artifact")

            run_id = create_run_index(
                db=db,
                project_id=project_id,
                snapshot_id=snapshot_id,
                scenario_id=sid,
                artifact_id=int(job.artifact_id),
                engine_version=engine_version,
                user_id=user_id,
            )

            run_ids.append(int(run_id))
            artifact_ids.append(int(job.artifact_id))

        # 2) run templates
        overrides_by_key = template_overrides or {}
        for key in template_keys:
            scenario = materialize_template(template_key=key, overrides=overrides_by_key.get(key) or {})

            job = create_job_and_run_sync(
                db=db,
                snapshot_id=snapshot_id,
                scenario=scenario,
                engine_version=engine_version,
            )
            if not job.artifact_id:
                raise HTTPException(500, "simulation did not produce artifact")

            run_id = create_run_index(
                db=db,
                project_id=project_id,
                snapshot_id=snapshot_id,
                scenario_id=None,  # template run
                artifact_id=int(job.artifact_id),
                engine_version=engine_version,
                user_id=user_id,
            )

            run_ids.append(int(run_id))
            artifact_ids.append(int(job.artifact_id))

        batch.status = "succeeded"
        batch.run_ids_json = json.dumps(run_ids)
        batch.artifact_ids_json = json.dumps(artifact_ids)
        db.add(batch)
        db.commit()
        db.refresh(batch)
        return batch

    except HTTPException as e:
        batch.status = "failed"
        batch.error = str(e.detail)
        batch.run_ids_json = json.dumps(run_ids)
        batch.artifact_ids_json = json.dumps(artifact_ids)
        db.add(batch)
        db.commit()
        db.refresh(batch)
        raise

    except Exception as e:
        batch.status = "failed"
        batch.error = f"batch failed: {e}"
        batch.run_ids_json = json.dumps(run_ids)
        batch.artifact_ids_json = json.dumps(artifact_ids)
        db.add(batch)
        db.commit()
        db.refresh(batch)
        raise HTTPException(500, "batch failed") from e


def get_batch(db: Session, batch_id: int) -> SimulationBatch | None:
    return db.query(SimulationBatch).filter(SimulationBatch.id == batch_id).first()
