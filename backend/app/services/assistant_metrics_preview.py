from __future__ import annotations

from typing import Any, Dict, List, Tuple
from fastapi import HTTPException

from app.services.performance_metrics import compute_performance_metrics
from app.services.proposal_hashing import compute_payload_hash


# Tools we allow preview for in Tier 4.6
PREVIEWABLE_TUNING_TOOLS = {
    "UPDATE_ENGINE_CONFIG",
    "UPDATE_SUSPENSION_CONFIG",
    "UPDATE_WHEEL_SETUP",
}


def _apply_payload_sandbox(*, tuning_state: Dict[str, Any], tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pure sandbox "apply" that returns a NEW tuning_state dict.
    No DB. No mutation of input dict.
    """
    tuning = dict(tuning_state or {})
    payload = dict(payload or {})

    if tool == "UPDATE_ENGINE_CONFIG":
        tuning["engine"] = payload
        return tuning

    if tool == "UPDATE_SUSPENSION_CONFIG":
        tuning["suspension"] = payload
        return tuning

    if tool == "UPDATE_WHEEL_SETUP":
        tuning["wheels"] = payload
        return tuning

    raise HTTPException(422, f"Tool not previewable: {tool}")


def _diff_numeric(baseline: Dict[str, Any], preview: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simple diff:
    for numeric fields present in both, compute preview - baseline.
    """
    diff: Dict[str, Any] = {}
    for k in baseline.keys() | preview.keys():
        b = baseline.get(k)
        p = preview.get(k)
        if isinstance(b, (int, float)) and isinstance(p, (int, float)):
            diff[k] = float(p) - float(b)
        elif b != p:
            diff[k] = {"from": b, "to": p}
    return diff


def _risk_notes_from_diff(diff: Dict[str, Any]) -> List[str]:
    """
    Deterministic rule-set.
    Keep conservative; no AI.
    """
    notes: List[str] = []

    # Example thresholds (tweak later, still deterministic)
    d0_100 = diff.get("est_0_100_kph_seconds")
    if isinstance(d0_100, (int, float)) and d0_100 < -1.5:
        notes.append("Large acceleration improvement detected; verify drivetrain and traction assumptions.")

    d_top = diff.get("est_top_speed_kph")
    if isinstance(d_top, (int, float)) and d_top > 25:
        notes.append("Top speed increased significantly; verify aero/drag assumptions and tire rating.")

    d_ptw = diff.get("power_to_weight_hp_per_ton")
    if isinstance(d_ptw, (int, float)) and d_ptw > 40:
        notes.append("Power-to-weight increased significantly; consider braking and handling implications.")

    # If nothing triggers
    if not notes:
        notes.append("No major risk flags detected from deterministic thresholds.")

    return notes


def preview_metrics_for_proposal(
    *,
    snapshot_id: int,
    tool: str,
    payload: Dict[str, Any],
    tuning_state: Dict[str, Any],
    vehicle_constants: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    if tool not in PREVIEWABLE_TUNING_TOOLS:
        raise HTTPException(422, "Tool not previewable")

    baseline = compute_performance_metrics(
        tuning_state=tuning_state or {},
        vehicle=vehicle_constants or None,
    )
    sandbox_tuning = _apply_payload_sandbox(
        tuning_state=tuning_state or {},
        tool=tool,
        payload=payload or {},
    )
    preview = compute_performance_metrics(
        tuning_state=sandbox_tuning,
        vehicle=vehicle_constants or None,
    )

    baseline_dict = {
        "power_hp": baseline.power_hp,
        "torque_nm": baseline.torque_nm,
        "power_to_weight_hp_per_ton": baseline.power_to_weight_hp_per_ton,
        "est_0_100_kph_seconds": baseline.est_0_100_kph_seconds,
        "est_top_speed_kph": baseline.est_top_speed_kph,
        "handling_index": baseline.handling_index,
        "braking_index": baseline.braking_index,
        "confidence": baseline.confidence,
        "notes": baseline.notes,
    }

    preview_dict = {
        "power_hp": preview.power_hp,
        "torque_nm": preview.torque_nm,
        "power_to_weight_hp_per_ton": preview.power_to_weight_hp_per_ton,
        "est_0_100_kph_seconds": preview.est_0_100_kph_seconds,
        "est_top_speed_kph": preview.est_top_speed_kph,
        "handling_index": preview.handling_index,
        "braking_index": preview.braking_index,
        "confidence": preview.confidence,
        "notes": preview.notes,
    }

    diff = _diff_numeric(baseline_dict, preview_dict)
    risk_notes = _risk_notes_from_diff(diff)

    payload_hash = compute_payload_hash(
        snapshot_id=snapshot_id,
        tool=tool,
        payload=payload or {},
    )

    return {
        "baseline": baseline_dict,
        "preview": preview_dict,
        "diff": diff,
        "risk_notes": risk_notes,
        "payload_hash": payload_hash,
    }

