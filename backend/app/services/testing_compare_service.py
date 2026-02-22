from __future__ import annotations

from typing import Any, Dict
from app.services.performance_metrics import compute_performance_metrics

def _shallow_delta(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic delta helper:
    - Only compares top-level numeric keys if present
    - Falls back to { "changed": True/False } for non-numerics
    """
    out: Dict[str, Any] = {}
    keys = set(a.keys()) | set(b.keys())
    for k in sorted(keys):
        av = a.get(k)
        bv = b.get(k)
        if isinstance(av, (int, float)) and isinstance(bv, (int, float)):
            out[k] = float(bv) - float(av)
        else:
            out[k] = {"from": av, "to": bv, "changed": av != bv}
    return out

def compare_snapshots(*, snapshot_a, snapshot_b, vehicle_a=None, vehicle_b=None) -> Dict[str, Any]:
    tuning_a = snapshot_a.tuning_state or {}
    tuning_b = snapshot_b.tuning_state or {}

    m_a = compute_performance_metrics(tuning_state=tuning_a, vehicle=vehicle_a or {})
    m_b = compute_performance_metrics(tuning_state=tuning_b, vehicle=vehicle_b or {})

    metrics_a = {
        "power_hp": m_a.power_hp,
        "torque_nm": m_a.torque_nm,
        "power_to_weight_hp_per_ton": m_a.power_to_weight_hp_per_ton,
        "est_0_100_kph_seconds": m_a.est_0_100_kph_seconds,
        "est_top_speed_kph": m_a.est_top_speed_kph,
        "handling_index": m_a.handling_index,
        "braking_index": m_a.braking_index,
        "confidence": m_a.confidence,
    }
    metrics_b = {
        "power_hp": m_b.power_hp,
        "torque_nm": m_b.torque_nm,
        "power_to_weight_hp_per_ton": m_b.power_to_weight_hp_per_ton,
        "est_0_100_kph_seconds": m_b.est_0_100_kph_seconds,
        "est_top_speed_kph": m_b.est_top_speed_kph,
        "handling_index": m_b.handling_index,
        "braking_index": m_b.braking_index,
        "confidence": m_b.confidence,
    }

    return {
        "a": {"snapshot_id": snapshot_a.id, "tuning": tuning_a, "metrics": metrics_a},
        "b": {"snapshot_id": snapshot_b.id, "tuning": tuning_b, "metrics": metrics_b},
        "deltas": {
            "tuning_delta": _shallow_delta(tuning_a, tuning_b),
            "metrics_delta": _shallow_delta(metrics_a, metrics_b),
        },
    }
