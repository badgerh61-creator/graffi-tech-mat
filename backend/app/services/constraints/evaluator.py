from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ConstraintViolation:
    constraint_id: str
    kind: str
    message: str
    data: Dict[str, Any]
    target_id: Optional[str] = None


def _get_constraints(snapshot) -> List[Dict[str, Any]]:
    body = snapshot.body_state or {}
    raw = body.get("constraints", [])
    return raw if isinstance(raw, list) else []


def evaluate_constraints_for_tool(
    *,
    snapshot,
    tool: str,
    payload: Dict[str, Any],
) -> List[ConstraintViolation]:
    """
    Deterministic, pure evaluation of constraints.
    Returns violations (empty => ok).
    """
    target_id = (payload or {}).get("target_id")
    if not target_id:
        return []

    constraints = _get_constraints(snapshot)
    violations: List[ConstraintViolation] = []

    for c in constraints:
        if not isinstance(c, dict):
            continue
        if c.get("enabled", True) is False:
            continue
        if c.get("target_id") != target_id:
            continue

        kind = str(c.get("kind") or "")
        cid = str(c.get("id") or "unknown")
        params = c.get("params") or {}

        if kind == "locked_axis":
            v = _eval_locked_axis(cid, tool, payload, params, target_id)
            if v:
                violations.append(v)

        elif kind == "bounds":
            v = _eval_bounds(cid, tool, payload, params, target_id)
            if v:
                violations.append(v)

        elif kind == "symmetry":
            v = _eval_symmetry(cid, tool, payload, params, target_id)
            if v:
                violations.append(v)

    return violations


def _eval_locked_axis(
    cid: str,
    tool: str,
    payload: Dict[str, Any],
    params: Dict[str, Any],
    target_id: Optional[str],
):
    tools = params.get("tools") or ["TRANSLATE", "ROTATE", "SCALE"]
    axes = params.get("axes") or []
    if tool not in tools:
        return None

    axis = str(payload.get("axis") or "")
    if axis in axes:
        return ConstraintViolation(
            constraint_id=cid,
            kind="locked_axis",
            message=f"{tool} blocked on axis {axis}",
            data={
                "axis": axis,
                "tool": tool,
                "target_id": target_id,
            },
            target_id=target_id,
        )
    return None


def _eval_bounds(
    cid: str,
    tool: str,
    payload: Dict[str, Any],
    params: Dict[str, Any],
    target_id: Optional[str],
):
    if tool != "TRANSLATE":
        return None

    bounds_min = (params.get("min") or {})
    bounds_max = (params.get("max") or {})

    d = payload.get("delta") or {}
    dx, dy, dz = float(d.get("x", 0)), float(d.get("y", 0)), float(d.get("z", 0))

    def out(v, lo, hi):
        return v < lo or v > hi

    lo_x = float(bounds_min.get("x", -1e9))
    lo_y = float(bounds_min.get("y", -1e9))
    lo_z = float(bounds_min.get("z", -1e9))
    hi_x = float(bounds_max.get("x", 1e9))
    hi_y = float(bounds_max.get("y", 1e9))
    hi_z = float(bounds_max.get("z", 1e9))

    if out(dx, lo_x, hi_x) or out(dy, lo_y, hi_y) or out(dz, lo_z, hi_z):
        return ConstraintViolation(
            constraint_id=cid,
            kind="bounds",
            message="Translate delta violates bounds",
            data={
                "delta": {"x": dx, "y": dy, "z": dz},
                "min": bounds_min,
                "max": bounds_max,
                "target_id": target_id,
            },
            target_id=target_id,
        )

    return None


def _eval_symmetry(
    cid: str,
    tool: str,
    payload: Dict[str, Any],
    params: Dict[str, Any],
    target_id: Optional[str],
):
    if tool != "TRANSLATE":
        return None

    plane = str(params.get("plane") or "")
    if plane != "vehicle_centerline":
        return None

    d = payload.get("delta") or {}
    dx = float(d.get("x", 0))
    if dx != 0:
        return ConstraintViolation(
            constraint_id=cid,
            kind="symmetry",
            message="Centerline symmetry forbids X translation",
            data={
                "plane": plane,
                "x": dx,
                "target_id": target_id,
            },
            target_id=target_id,
        )
    return None
