from __future__ import annotations

from typing import Dict, Any, Set
from fastapi import HTTPException

VALID_AXIS_LOCKS = {"x", "y", "z", "xy", "xz", "yz", "xyz"}


def normalize_axis_lock(axis_lock: str | None) -> str:
    if axis_lock is None:
        return "xyz"
    if not isinstance(axis_lock, str):
        raise HTTPException(422, "axis_lock must be a string")
    if axis_lock not in VALID_AXIS_LOCKS:
        raise HTTPException(422, "invalid axis_lock")
    return axis_lock


def apply_axis_lock_to_payload(*, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pure helper. Returns a new dict.
    Drops disallowed axes from payload.
    """
    p = dict(payload or {})
    axis_lock = normalize_axis_lock(p.get("axis_lock"))
    p["axis_lock"] = axis_lock

    allowed: Set[str] = set(axis_lock)  # "xy" => {"x","y"}

    for axis in ("x", "y", "z"):
        if axis in p and axis not in allowed:
            p.pop(axis, None)

    return p
