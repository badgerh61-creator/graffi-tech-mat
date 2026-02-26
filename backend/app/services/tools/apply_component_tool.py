from __future__ import annotations
from typing import Any, Dict, List

from app.services.components.store import find_component, upsert_component
from app.services.components.compiler import compile_component_ops
from app.services.constraints.evaluator import evaluate_constraints_for_tool

def evaluate_apply_component(*, snapshot, payload: Dict[str, Any]) -> Dict[str, Any]:
    component_id = str(payload.get("component_id") or "")
    if not component_id:
        return {"ok": False, "violations": [], "error": "component_id required"}

    current = find_component(snapshot, component_id)
    if not current:
        return {"ok": False, "violations": [], "error": "component not found"}

    next_params = payload.get("next_params") or {}
    target_id = payload.get("target_id") or current.get("target_id")

    kind = current.get("kind") or "custom"
    ops = compile_component_ops(kind=kind, params=next_params, target_id=target_id)

    violations = []
    for op in ops:
        v = evaluate_constraints_for_tool(
            snapshot=snapshot,
            tool=op["tool"],
            payload=op["payload"],
        )
        violations.extend(v)

    return {
        "ok": len(violations) == 0,
        "ops": ops,
        "violations": [vv.__dict__ for vv in violations],
    }

def apply_apply_component(*, snapshot, payload: Dict[str, Any], tool_executor) -> Dict[str, Any]:
    """
    tool_executor: your existing governed executor for TRANSLATE/ROTATE/SCALE
    """
    component_id = str(payload.get("component_id") or "")
    current = find_component(snapshot, component_id)
    if not current:
        raise RuntimeError("component not found")

    next_params = payload.get("next_params") or {}
    target_id = payload.get("target_id") or current.get("target_id")

    kind = current.get("kind") or "custom"
    ops = compile_component_ops(kind=kind, params=next_params, target_id=target_id)

    # apply component state first (so snapshot records intent)
    next_component = {
        **current,
        "params": next_params,
        "target_id": target_id,
        "version": int(current.get("version") or 1),
        "enabled": bool(current.get("enabled", True)),
    }
    upsert_component(snapshot, next_component)

    # execute compiled ops using your existing pipeline
    for op in ops:
        tool_executor(
            tool=op["tool"],
            station=op["station"],
            payload=op["payload"],
        )

    return {"ok": True, "applied_ops": ops, "component_id": component_id}
