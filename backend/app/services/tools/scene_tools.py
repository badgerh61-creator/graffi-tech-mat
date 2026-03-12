from __future__ import annotations

from typing import Any, Dict
from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.asset import Asset
from app.models.model import ModelRecord
from app import crud

from app.services.mutations.scene_objects import (
    validate_add_model_ref,
    apply_add_model_ref,
    validate_remove_object,
    apply_remove_object,
    validate_set_object_enabled,
    apply_set_object_enabled,
    validate_set_object_layers,
    apply_set_object_layers,
)

# Tool names (Tier 7.46 + 7.47)
SCENE_ADD_MODEL_REF = "SCENE_ADD_MODEL_REF"
SCENE_REMOVE_OBJECT = "SCENE_REMOVE_OBJECT"
SCENE_SET_OBJECT_ENABLED = "SCENE_SET_OBJECT_ENABLED"
SCENE_SET_OBJECT_LAYERS = "SCENE_SET_OBJECT_LAYERS"


def _require_asset_access(*, db: Session, user_id: int, asset_id: int) -> None:
    """
    Reuse your existing access model:
    - asset is linked to a model
    - user must have access to that model
    """
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


def evaluate_scene_tool(*, db: Session, user, tool: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate should be read-only (no snapshot writes).
    It may check permissions + payload validity.
    """
    if tool == SCENE_ADD_MODEL_REF:
        err = validate_add_model_ref(payload)
        if err:
            return {"ok": False, "error": err}

        asset_id = int(payload["asset_id"])
        _require_asset_access(db=db, user_id=int(user.id), asset_id=asset_id)
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

    return {"ok": False, "error": "unknown scene tool"}


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

    return {"ok": False, "error": "unknown scene tool"}
