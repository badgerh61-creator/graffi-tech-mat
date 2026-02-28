from __future__ import annotations
from typing import Any, Dict

from app.services.decals.mutator import (
    validate_create, validate_update, validate_delete,
    apply_create, apply_update, apply_delete
)

def evaluate_decal_tool(*, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "DECAL_CREATE":
        err = validate_create(payload)
        return {"ok": err is None, "error": err}
    if tool == "DECAL_UPDATE":
        err = validate_update(payload)
        return {"ok": err is None, "error": err}
    if tool == "DECAL_DELETE":
        err = validate_delete(payload)
        return {"ok": err is None, "error": err}
    return {"ok": False, "error": "unknown decal tool"}

def apply_decal_tool(*, snapshot, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "DECAL_CREATE":
        return apply_create(snapshot, payload)
    if tool == "DECAL_UPDATE":
        return apply_update(snapshot, payload)
    if tool == "DECAL_DELETE":
        return apply_delete(snapshot, payload)
    return {"ok": False, "error": "unknown decal tool"}
