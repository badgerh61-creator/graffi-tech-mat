from __future__ import annotations

from typing import Any, Dict

from app.services.decals.mutator import (
    validate_create,
    validate_update,
    validate_delete,
    validate_set_asset,
    apply_create,
    apply_update,
    apply_delete,
    apply_set_asset,
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

    # Tier 7.44 — Asset assignment
    # Accept both asset_ref and asset_id (alias)
    if tool == "DECAL_SET_ASSET":
        if "asset_ref" not in payload and "asset_id" in payload:
            payload = {**payload, "asset_ref": payload.get("asset_id")}
        err = validate_set_asset(payload)
        return {"ok": err is None, "error": err}

    return {"ok": False, "error": "unknown decal tool"}


def apply_decal_tool(*, snapshot, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if tool == "DECAL_CREATE":
        return apply_create(snapshot, payload)

    if tool == "DECAL_UPDATE":
        return apply_update(snapshot, payload)

    if tool == "DECAL_DELETE":
        return apply_delete(snapshot, payload)

    if tool == "DECAL_SET_ASSET":
        if "asset_ref" not in payload and "asset_id" in payload:
            payload = {**payload, "asset_ref": payload.get("asset_id")}
        return apply_set_asset(snapshot, payload)

    return {"ok": False, "error": "unknown decal tool"}
