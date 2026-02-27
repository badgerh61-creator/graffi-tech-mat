from __future__ import annotations

from typing import Any, Dict, List
from fastapi import HTTPException


def _nums(xs: Any) -> List[float]:
    if xs is None:
        return []
    if not isinstance(xs, list):
        raise HTTPException(422, "curve must be a list")
    out: List[float] = []
    for v in xs:
        try:
            f = float(v)
            if f == f:  # not NaN
                out.append(f)
        except Exception:
            continue
    return out


def _avg(xs: List[float]) -> float:
    return (sum(xs) / float(len(xs))) if xs else 0.0


def _max(xs: List[float]) -> float:
    return max(xs) if xs else 0.0


def _min(xs: List[float]) -> float:
    return min(xs) if xs else 0.0


def compute_summary(*, curves: Dict[str, Any], timestep_s: float, duration_s: float) -> Dict[str, float]:
    speed = _nums(curves.get("speed_mps"))
    rpm = _nums(curves.get("rpm"))
    temp = _nums(curves.get("engine_temp_c"))
    grip = _nums(curves.get("grip"))

    return {
        "duration_s": float(duration_s),
        "timestep_s": float(timestep_s),

        "speed_max_mps": float(_max(speed)),
        "speed_avg_mps": float(_avg(speed)),

        "rpm_max": float(_max(rpm)),
        "rpm_avg": float(_avg(rpm)),

        "engine_temp_max_c": float(_max(temp)),
        "engine_temp_avg_c": float(_avg(temp)),

        "grip_min": float(_min(grip)) if grip else 0.0,
        "grip_avg": float(_avg(grip)),
    }


def compute_delta(*, a_summary: Dict[str, float], b_summary: Dict[str, float]) -> Dict[str, float]:
    keys = [
        "speed_max_mps", "speed_avg_mps",
        "rpm_max", "rpm_avg",
        "engine_temp_max_c", "engine_temp_avg_c",
        "grip_min", "grip_avg",
    ]
    return {k: float(b_summary.get(k, 0.0) - a_summary.get(k, 0.0)) for k in keys}


def export_csv(*, curves: Dict[str, Any]) -> str:
    time_s = _nums(curves.get("time_s"))
    speed = _nums(curves.get("speed_mps"))
    rpm = _nums(curves.get("rpm"))
    temp = _nums(curves.get("engine_temp_c"))
    grip = _nums(curves.get("grip"))

    n = min(len(time_s), len(speed), len(rpm), len(temp), len(grip))
    lines = ["time_s,speed_mps,rpm,engine_temp_c,grip"]
    for i in range(n):
        lines.append(f"{time_s[i]},{speed[i]},{rpm[i]},{temp[i]},{grip[i]}")
    return "\n".join(lines) + "\n"
