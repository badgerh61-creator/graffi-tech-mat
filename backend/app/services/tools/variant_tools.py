from __future__ import annotations
from typing import Dict, Any
from app.services.variants.mutator import (
    validate_save_variant,
    apply_save_variant,
    validate_apply_variant,
    apply_apply_variant,
    validate_delete_variant,
    apply_delete_variant,
)

def evaluate_variant_tool(*, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "VARIANT_SAVE":
        err = validate_save_variant(payload)
        return {"ok": err is None, "error": err}

    if tool == "VARIANT_APPLY":
        err = validate_apply_variant(payload)
        return {"ok": err is None, "error": err}

    if tool == "VARIANT_DELETE":
        err = validate_delete_variant(payload)
        return {"ok": err is None, "error": err}

    return {"ok": False, "error": "unknown variant tool"}

def apply_variant_tool(*, snapshot, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "VARIANT_SAVE":
        return apply_save_variant(snapshot, payload)

    if tool == "VARIANT_APPLY":
        return apply_apply_variant(snapshot, payload)

    if tool == "VARIANT_DELETE":
        return apply_delete_variant(snapshot, payload)

    return {"ok": False, "error": "unknown variant tool"}
