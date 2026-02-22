from __future__ import annotations

from typing import Any, Dict, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.testing_scenarios_catalog import get_scenario
from app.services.performance_metrics import compute_performance_metrics
from app.models.testing_result import TestingResult

def build_summary(metrics: Dict[str, Any]) -> str:
    # Stable, deterministic summary string (no timestamps inside)
    return (
        f"Est 0–100 kph: {metrics.get('est_0_100_kph_seconds')}s, "
        f"Top speed: {metrics.get('est_top_speed_kph')}kph, "
        f"P/W: {metrics.get('power_to_weight_hp_per_ton')} hp/ton, "
        f"Confidence: {metrics.get('confidence')}"
    )

def enqueue_testing_run(*, db: Session, snapshot, user_id: int, scenario_id: str) -> str:
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    # If you already have an async job system, create a job there and return its id.
    # Stub: return a deterministic placeholder job id.
    # Replace with: jobs.create(...).
    return f"job-testing-{snapshot.id}-{scenario_id}"

def materialize_testing_result_now(*, db: Session, snapshot, user_id: int, scenario_id: str) -> TestingResult:
    """
    Optional synchronous materialization helper (useful in dev/tests).
    In production, your worker would call this from the job processor.
    """
    scenario = get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(404, "Scenario not found")

    # Pure deterministic compute from Tier 4.4
    vehicle = {"mass_kg": getattr(snapshot, "vehicle_mass_kg", None)}
    m = compute_performance_metrics(tuning_state=snapshot.tuning_state or {}, vehicle=vehicle)

    metrics_dict = {
        "power_hp": m.power_hp,
        "torque_nm": m.torque_nm,
        "power_to_weight_hp_per_ton": m.power_to_weight_hp_per_ton,
        "est_0_100_kph_seconds": m.est_0_100_kph_seconds,
        "est_top_speed_kph": m.est_top_speed_kph,
        "handling_index": m.handling_index,
        "braking_index": m.braking_index,
        "notes": m.notes,
        "confidence": m.confidence,
    }

    result = TestingResult(
        snapshot_id=snapshot.id,
        scenario_id=scenario_id,
        metrics=metrics_dict,
        summary=build_summary(metrics_dict),
        deltas=None,
        job_id=None,
        created_by_user_id=user_id,
    )

    db.add(result)
    db.commit()
    db.refresh(result)
    return result

def get_result(*, db: Session, result_id: int) -> Optional[TestingResult]:
    return db.query(TestingResult).get(result_id)
