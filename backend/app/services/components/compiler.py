from __future__ import annotations
from typing import Any, Dict, List, Optional

def compile_component_ops(
    *,
    kind: str,
    params: Dict[str, Any],
    target_id: Optional[str],
) -> List[Dict[str, Any]]:
    """
    Deterministic compilation of a component into normal tool ops.
    Tier 7.33 minimal set:
      - ride_height -> TRANSLATE on Y
      - wheel_scale -> SCALE uniform
      - spoiler_angle -> ROTATE on X
    """
    kind = str(kind or "custom")
    params = params or {}

    ops: List[Dict[str, Any]] = []

    if kind == "ride_height":
        # params: { "delta_y": number }
        dy = float(params.get("delta_y", 0))
        if target_id:
            ops.append({
                "tool": "TRANSLATE",
                "station": "geometry",
                "payload": {
                    "target_id": target_id,
                    "axis": "y",
                    "delta": {"x": 0, "y": dy, "z": 0},
                    "snap": {"enabled": False, "step": 0},
                },
            })

    elif kind == "wheel_scale":
        # params: { "factor": number }
        f = float(params.get("factor", 1.0))
        if target_id:
            ops.append({
                "tool": "SCALE",
                "station": "geometry",
                "payload": {
                    "target_id": target_id,
                    "axis": "uniform",
                    "factor": f,
                    "snap": {"enabled": False, "step_factor": 0},
                },
            })

    elif kind == "spoiler_angle":
        # params: { "degrees": number }
        deg = float(params.get("degrees", 0))
        if target_id:
            ops.append({
                "tool": "ROTATE",
                "station": "geometry",
                "payload": {
                    "target_id": target_id,
                    "axis": "x",
                    "degrees": deg,
                    "snap": {"enabled": False, "step_degrees": 0},
                },
            })

    # Unknown kinds compile to no-ops (safe)
    return ops
