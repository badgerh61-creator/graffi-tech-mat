from __future__ import annotations
from typing import Dict, Any
from app.services.materials.paint_mutator import (
    validate_apply_library_preset,
    apply_apply_library_preset,
    validate_save_swatch,
    apply_save_swatch,
    validate_delete_swatch,
    apply_delete_swatch,
    validate_apply_swatch,
    apply_apply_swatch,
)

def evaluate_paint_tool(*, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "PAINT_APPLY_LIBRARY_PRESET":
        err = validate_apply_library_preset(payload)
        return {"ok": err is None, "error": err}

    if tool == "PAINT_SAVE_SWATCH":
        err = validate_save_swatch(payload)
        return {"ok": err is None, "error": err}

    if tool == "PAINT_DELETE_SWATCH":
        err = validate_delete_swatch(payload)
        return {"ok": err is None, "error": err}

    if tool == "PAINT_APPLY_SWATCH":
        err = validate_apply_swatch(payload)
        return {"ok": err is None, "error": err}

    return {"ok": False, "error": "unknown paint tool"}

def apply_paint_tool(*, snapshot, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "PAINT_APPLY_LIBRARY_PRESET":
        return apply_apply_library_preset(snapshot, payload)

    if tool == "PAINT_SAVE_SWATCH":
        return apply_save_swatch(snapshot, payload)

    if tool == "PAINT_DELETE_SWATCH":
        return apply_delete_swatch(snapshot, payload)

    if tool == "PAINT_APPLY_SWATCH":
        return apply_apply_swatch(snapshot, payload)

    return {"ok": False, "error": "unknown paint tool"}
