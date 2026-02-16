from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


@dataclass(frozen=True)
class PerformanceMetrics:
    power_hp: float
    torque_nm: float
    power_to_weight_hp_per_ton: float
    est_0_100_kph_seconds: float
    est_top_speed_kph: float
    handling_index: float
    braking_index: float
    notes: List[str]
    confidence: float


def compute_performance_metrics(*, tuning_state: Dict[str, Any], vehicle: Dict[str, Any] | None = None) -> PerformanceMetrics:
    """
    Deterministic, pure computation.
    Never mutates inputs.
    """
    vehicle = dict(vehicle or {})
    tuning = dict(tuning_state or {})

    notes: List[str] = []
    confidence = 1.0

    engine = tuning.get("engine") or {}
    mass_kg = float(vehicle.get("mass_kg") or 1400.0)

    # --- basic power/torque defaults (degrade gracefully)
    power_hp = engine.get("power_hp")
    torque_nm = engine.get("torque_nm")

    if power_hp is None:
        power_hp = 120.0
        notes.append("Engine power_hp missing; using conservative default.")
        confidence *= 0.75

    if torque_nm is None:
        torque_nm = 180.0
        notes.append("Engine torque_nm missing; using conservative default.")
        confidence *= 0.85

    power_hp = float(power_hp)
    torque_nm = float(torque_nm)

    # --- derived metrics
    hp_per_ton = power_hp / (mass_kg / 1000.0)

    # crude deterministic estimates (no sim)
    est_0_100 = max(2.5, 14.0 - (hp_per_ton * 0.05))
    est_top_speed = max(120.0, 160.0 + (power_hp * 0.15))

    # simple indices from tuning knobs
    suspension = tuning.get("suspension") or {}
    tires = tuning.get("wheels") or {}

    handling = float(suspension.get("handling_index") or 0.5)
    braking = float(tires.get("braking_index") or 0.5)

    if "handling_index" not in suspension:
        notes.append("Suspension handling_index missing; using default.")
        confidence *= 0.9

    if "braking_index" not in tires:
        notes.append("Wheel braking_index missing; using default.")
        confidence *= 0.9

    confidence = max(0.1, min(1.0, confidence))

    return PerformanceMetrics(
        power_hp=power_hp,
        torque_nm=torque_nm,
        power_to_weight_hp_per_ton=hp_per_ton,
        est_0_100_kph_seconds=est_0_100,
        est_top_speed_kph=est_top_speed,
        handling_index=handling,
        braking_index=braking,
        notes=notes,
        confidence=confidence,
    )

