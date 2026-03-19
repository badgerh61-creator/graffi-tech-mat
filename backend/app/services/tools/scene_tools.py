from __future__ import annotations

from typing import Any, Dict
from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.asset import Asset
from app.models.model import ModelRecord
from app import crud

try:
    from app.services.mutations.scene_objects import (
        validate_add_model_ref,
        apply_add_model_ref,
        validate_remove_object,
        apply_remove_object,
        validate_set_object_enabled,
        apply_set_object_enabled,
        validate_set_object_layers,
        apply_set_object_layers,
        validate_duplicate_object,
        apply_duplicate_object,
        validate_mirror_object,
        apply_mirror_object,
        validate_create_group,
        apply_create_group,
        validate_parent_object,
        apply_parent_object,
        validate_unparent_object,
        apply_unparent_object,
        validate_bulk_set_enabled,
        apply_bulk_set_enabled,
        validate_bulk_set_layers,
        apply_bulk_set_layers,
        # --- Pivot tools ---
        validate_set_object_pivot,
        apply_set_object_pivot,
        validate_reset_object_pivot,
        apply_reset_object_pivot,
        validate_set_object_pivot_preset,
        apply_set_object_pivot_preset,
    )
except ImportError:
    from app.services.scene_objects.mutator import (
        validate_add_model_ref,
        apply_add_model_ref,
        validate_remove_object,
        apply_remove_object,
        validate_set_object_enabled,
        apply_set_object_enabled,
        validate_set_object_layers,
        apply_set_object_layers,
        validate_duplicate_object,
        apply_duplicate_object,
        validate_mirror_object,
        apply_mirror_object,
        validate_create_group,
        apply_create_group,
        validate_parent_object,
        apply_parent_object,
        validate_unparent_object,
        apply_unparent_object,
        validate_bulk_set_enabled,
        apply_bulk_set_enabled,
        validate_bulk_set_layers,
        apply_bulk_set_layers,
        # --- Pivot tools ---
        validate_set_object_pivot,
        apply_set_object_pivot,
        validate_reset_object_pivot,
        apply_reset_object_pivot,
        validate_set_object_pivot_preset,
        apply_set_object_pivot_preset,
    )

# --- Tool constants ---
SCENE_ADD_MODEL_REF = "SCENE_ADD_MODEL_REF"
SCENE_REMOVE_OBJECT = "SCENE_REMOVE_OBJECT"
SCENE_SET_OBJECT_ENABLED = "SCENE_SET_OBJECT_ENABLED"
SCENE_SET_OBJECT_LAYERS = "SCENE_SET_OBJECT_LAYERS"

SCENE_DUPLICATE_OBJECT = "SCENE_DUPLICATE_OBJECT"
SCENE_MIRROR_OBJECT = "SCENE_MIRROR_OBJECT"

SCENE_CREATE_GROUP = "SCENE_CREATE_GROUP"
SCENE_PARENT_OBJECT = "SCENE_PARENT_OBJECT"
SCENE_UNPARENT_OBJECT = "SCENE_UNPARENT_OBJECT"

SCENE_BULK_SET_ENABLED = "SCENE_BULK_SET_ENABLED"
SCENE_BULK_SET_LAYERS = "SCENE_BULK_SET_LAYERS"

# --- Pivot tool constants ---
SCENE_SET_OBJECT_PIVOT = "SCENE_SET_OBJECT_PIVOT"
SCENE_RESET_OBJECT_PIVOT = "SCENE_RESET_OBJECT_PIVOT"
SCENE_SET_OBJECT_PIVOT_PRESET = "SCENE_SET_OBJECT_PIVOT_PRESET"


# --- Access control helpers ---
def _require_asset_access(*, db: Session, user_id: int, asset_id: int) -> None:
    asset = (
        db.query(Asset)
        .join(ModelRecord)
        .filter(Asset.id == asset_id)
        .first()
    )
    if not asset:
        raise HTTPException(404, "Asset not found")

    model = crud.get_model_if_accessible(db, model_id=asset.model_id, user_id=user_id)
    if not model:
        raise HTTPException(403, "No access to asset")


def _maybe_require_asset_access(*, db: Session, user, payload: Dict[str, Any]) -> None:
    raw_asset_id = payload.get("asset_id")
    if raw_asset_id is None:
        return

    try:
        asset_id = int(raw_asset_id)
    except (TypeError, ValueError):
        return

    _require_asset_access(db=db, user_id=int(user.id), asset_id=asset_id)


# --- Evaluator ---
def evaluate_scene_tool(*, db: Session, user, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate should be read-only (no snapshot writes).
    It may check permissions + payload validity.
    """
    if tool == SCENE_ADD_MODEL_REF:
        err = validate_add_model_ref(payload)
        if err:
            return {"ok": False, "error": err}
        _maybe_require_asset_access(db=db, user=user, payload=payload)
        return {"ok": True}

    if tool == SCENE_REMOVE_OBJECT:
        err = validate_remove_object(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_SET_OBJECT_ENABLED:
        err = validate_set_object_enabled(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_SET_OBJECT_LAYERS:
        err = validate_set_object_layers(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_DUPLICATE_OBJECT:
        err = validate_duplicate_object(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_MIRROR_OBJECT:
        err = validate_mirror_object(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_CREATE_GROUP:
        err = validate_create_group(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_PARENT_OBJECT:
        err = validate_parent_object(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_UNPARENT_OBJECT:
        err = validate_unparent_object(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_BULK_SET_ENABLED:
        err = validate_bulk_set_enabled(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    if tool == SCENE_BULK_SET_LAYERS:
        err = validate_bulk_set_layers(payload)
        if err:
            return {"ok": False, "error": err}
        return {"ok": True}

    # --- Pivot tools ---
    if tool == SCENE_SET_OBJECT_PIVOT:
        err = validate_set_object_pivot(payload)
        return {"ok": err is None, "error": err}

    if tool == SCENE_RESET_OBJECT_PIVOT:
        err = validate_reset_object_pivot(payload)
        return {"ok": err is None, "error": err}

    if tool == SCENE_SET_OBJECT_PIVOT_PRESET:
        err = validate_set_object_pivot_preset(payload)
        return {"ok": err is None, "error": err}

    return {"ok": False, "error": "unknown scene tool"}


# --- Applier ---
def apply_scene_tool(*, snapshot, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply mutates the snapshot in-memory (governed pipeline owns persistence).
    """
    if tool == SCENE_ADD_MODEL_REF:
        return apply_add_model_ref(snapshot, payload)

    if tool == SCENE_REMOVE_OBJECT:
        return apply_remove_object(snapshot, payload)

    if tool == SCENE_SET_OBJECT_ENABLED:
        return apply_set_object_enabled(snapshot, payload)

    if tool == SCENE_SET_OBJECT_LAYERS:
        return apply_set_object_layers(snapshot, payload)

    if tool == SCENE_DUPLICATE_OBJECT:
        return apply_duplicate_object(snapshot, payload)

    if tool == SCENE_MIRROR_OBJECT:
        return apply_mirror_object(snapshot, payload)

    if tool == SCENE_CREATE_GROUP:
        return apply_create_group(snapshot, payload)

    if tool == SCENE_PARENT_OBJECT:
        return apply_parent_object(snapshot, payload)

    if tool == SCENE_UNPARENT_OBJECT:
        return apply_unparent_object(snapshot, payload)

    if tool == SCENE_BULK_SET_ENABLED:
        return apply_bulk_set_enabled(snapshot, payload)

    if tool == SCENE_BULK_SET_LAYERS:
        return apply_bulk_set_layers(snapshot, payload)

    # --- Pivot tools ---
    if tool == SCENE_SET_OBJECT_PIVOT:
        return apply_set_object_pivot(snapshot, payload)

    if tool == SCENE_RESET_OBJECT_PIVOT:
        return apply_reset_object_pivot(snapshot, payload)

    if tool == SCENE_SET_OBJECT_PIVOT_PRESET:
        return apply_set_object_pivot_preset(snapshot, payload)

    return {"ok": False, "error": "unknown scene tool"}
