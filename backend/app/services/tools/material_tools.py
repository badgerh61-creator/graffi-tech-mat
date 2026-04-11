from __future__ import annotations
from typing import Dict, Any

from app.services.materials.mutator import (
    validate_set,
    validate_clear,
    validate_update_params,
    apply_set,
    apply_clear,
    apply_update_params,
    validate_set_slot,
    validate_clear_slot,
    apply_set_slot,
    apply_clear_slot,
)


def evaluate_material_tool(*, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # ✅ alias
    if tool in ("MATERIAL_SET_PRESET", "MATERIAL_APPLY_PRESET"):
        err = validate_set(payload)
        return {"ok": err is None, "error": err}

    if tool == "MATERIAL_CLEAR_OVERRIDE":
        err = validate_clear(payload)
        return {"ok": err is None, "error": err}

    if tool == "MATERIAL_UPDATE_PARAMS":
        err = validate_update_params(payload)
        return {"ok": err is None, "error": err}

    if tool == "MATERIAL_SET_SLOT_PRESET":
        err = validate_set_slot(payload)
        return {"ok": err is None, "error": err}

    if tool == "MATERIAL_CLEAR_SLOT_OVERRIDE":
        err = validate_clear_slot(payload)
        return {"ok": err is None, "error": err}

    return {"ok": False, "error": "unknown material tool"}


def apply_material_tool(*, snapshot, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # ✅ alias
    if tool in ("MATERIAL_SET_PRESET", "MATERIAL_APPLY_PRESET"):
        return apply_set(snapshot, payload)

    if tool == "MATERIAL_CLEAR_OVERRIDE":
        return apply_clear(snapshot, payload)

    if tool == "MATERIAL_UPDATE_PARAMS":
        return apply_update_params(snapshot, payload)

    if tool == "MATERIAL_SET_SLOT_PRESET":
        return apply_set_slot(snapshot, payload)

    if tool == "MATERIAL_CLEAR_SLOT_OVERRIDE":
        return apply_clear_slot(snapshot, payload)

    return {"ok": False, "error": "unknown material tool"}
