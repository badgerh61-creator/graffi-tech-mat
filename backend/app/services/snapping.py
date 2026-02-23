from __future__ import annotations

from typing import Dict, Any, Iterable
from fastapi import HTTPException


def _quantize(value: float, step: float) -> float:
    return round(value / step) * step


def apply_snapping_to_transform_payload(
    *,
    payload: Dict[str, Any],
    allowed_axes: Iterable[str] = ("x", "y", "z"),
) -> Dict[str, Any]:
    """
    Tier 7.3 — Pure helper.
    Does NOT write DB. Does NOT mutate input dict.
    """
    p = dict(payload or {})
    snap = bool(p.get("snap", False))
    if not snap:
        return p

    step = p.get("snap_step", None)
    if step is None:
        step = 0.1  # safe fallback
    try:
        step = float(step)
    except Exception:
        raise HTTPException(422, "snap_step must be a number")

    if step <= 0:
        raise HTTPException(422, "snap_step must be > 0")

    axes = p.get("snap_axes") or list(allowed_axes)
    if not isinstance(axes, list) or not all(isinstance(a, str) for a in axes):
        raise HTTPException(422, "snap_axes must be a list of strings")

    for axis in ("x", "y", "z"):
        if axis in axes and axis in p and p[axis] is not None:
            try:
                p[axis] = float(_quantize(float(p[axis]), step))
            except Exception:
                raise HTTPException(422, f"{axis} must be a number")

    return p
