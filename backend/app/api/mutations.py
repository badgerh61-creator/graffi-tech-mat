from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.models.mutation_journal import MutationJournal
from app.crud import require_model_role

from app.services.mutations.rename_asset import RenameAssetAdapter
from app.services.mutations.toggle_asset_visibility import (
    ToggleAssetVisibilityAdapter,
)
from app.services.mutations.set_preview_camera_preset import (
    SetPreviewCameraPresetAdapter,
)

router = APIRouter(prefix="/mutations", tags=["mutations"])


# ============================================================
# PHASE I.1 — Rename Asset (FROZEN)
# ============================================================

@router.post("/rename-asset")
def rename_asset(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    target_id = payload.get("targetId")
    previous_name = payload.get("previousName")
    next_name = payload.get("nextName")
    reason = payload.get("reason")

    if not target_id or not previous_name or not next_name:
        raise HTTPException(status_code=400, detail="Invalid payload")

    asset = db.query(Asset).filter(Asset.id == target_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    model = db.query(ModelRecord).filter(ModelRecord.id == asset.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    try:
        require_model_role(db, user=user, model=model, min_role="editor")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if asset.filename != previous_name:
        raise HTTPException(
            status_code=409,
            detail="Asset name out of date. Refresh required.",
        )

    journal = MutationJournal(
        intent_type="RenameAsset",
        target_type="asset",
        target_id=asset.id,
        before_state={"filename": previous_name},
        after_state={"filename": next_name},
        issued_by_user_id=user.id,
        reason=reason,
    )

    try:
        RenameAssetAdapter.execute(db, asset=asset, next_name=next_name)
        db.add(journal)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Rename failed")

    return {
        "status": "ok",
        "assetId": asset.id,
        "newName": next_name,
    }


# ============================================================
# PHASE I.2 — Toggle Asset Visibility (METADATA ONLY)
# ============================================================

@router.post("/toggle-asset-visibility")
def toggle_asset_visibility(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    target_id = payload.get("targetId")
    previous_value = payload.get("previousValue")
    next_value = payload.get("nextValue")
    reason = payload.get("reason")

    if target_id is None or previous_value is None or next_value is None:
        raise HTTPException(status_code=400, detail="Invalid payload")

    if not isinstance(previous_value, bool) or not isinstance(next_value, bool):
        raise HTTPException(
            status_code=400,
            detail="Visibility values must be boolean",
        )

    if previous_value == next_value:
        raise HTTPException(
            status_code=400,
            detail="Visibility must change",
        )

    asset = db.query(Asset).filter(Asset.id == target_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    model = db.query(ModelRecord).filter(ModelRecord.id == asset.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    try:
        require_model_role(db, user=user, model=model, min_role="editor")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if asset.is_visible != previous_value:
        raise HTTPException(
            status_code=409,
            detail="Asset visibility out of date. Refresh required.",
        )

    journal = MutationJournal(
        intent_type="ToggleAssetVisibility",
        target_type="asset",
        target_id=asset.id,
        before_state={"is_visible": previous_value},
        after_state={"is_visible": next_value},
        issued_by_user_id=user.id,
        reason=reason,
    )

    try:
        ToggleAssetVisibilityAdapter.execute(
            db,
            asset=asset,
            next_is_visible=next_value,
        )
        db.add(journal)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Visibility toggle failed",
        )

    return {
        "status": "ok",
        "assetId": asset.id,
        "isVisible": next_value,
    }


# ============================================================
# PHASE I.3 — Set Preview Camera Preset (METADATA ONLY)
# ============================================================

@router.post("/set-preview-camera-preset")
def set_preview_camera_preset(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    model_id = payload.get("modelId")
    previous_preset = payload.get("previousPreset")
    next_preset = payload.get("nextPreset")
    reason = payload.get("reason")

    # ---- 1. Validate payload ----
    if not model_id or not previous_preset or not next_preset:
        raise HTTPException(
            status_code=400,
            detail="Invalid payload",
        )

    if previous_preset == next_preset:
        raise HTTPException(
            status_code=400,
            detail="Preset must change",
        )

    # ---- 2. Load model ----
    model = (
        db.query(ModelRecord)
        .filter(ModelRecord.id == model_id)
        .first()
    )
    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found",
        )

    # ---- 3. Permission gate ----
    try:
        require_model_role(
            db,
            user=user,
            model=model,
            min_role="editor",
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    # ---- 4. Stale-state guard ----
    if model.preview_camera_preset_id != previous_preset:
        raise HTTPException(
            status_code=409,
            detail="Preview camera preset out of date. Refresh required.",
        )

    # ---- 5. Prepare journal ----
    journal = MutationJournal(
        intent_type="SetPreviewCameraPreset",
        target_type="model",
        target_id=model.id,
        before_state={"preset": previous_preset},
        after_state={"preset": next_preset},
        issued_by_user_id=user.id,
        reason=reason,
    )

    # ---- 6. Atomic mutation ----
    try:
        SetPreviewCameraPresetAdapter.execute(
            db,
            model=model,
            next_preset=next_preset,
        )
        db.add(journal)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update preview camera preset",
        )

    return {
        "status": "ok",
        "modelId": model.id,
        "previewCameraPreset": next_preset,
    }


# ============================================================
# PHASE I.6 — Generate Asset Thumbnail (VALIDATED)
# ============================================================

@router.post("/generate-asset-thumbnail")
def generate_asset_thumbnail(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    asset_id = payload.get("assetId")
    reason = payload.get("reason")

    if not asset_id:
        raise HTTPException(status_code=400, detail="Invalid payload")

    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    model = db.query(ModelRecord).filter(ModelRecord.id == asset.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # ---- Permission gate ----
    try:
        require_model_role(db, user=user, model=model, min_role="editor")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    # ---- 🔒 HARD TYPE GUARD (THE FIX) ----
    if asset.content_type not in {
        "image/png",
        "image/jpeg",
        "image/webp",
    }:
        raise HTTPException(
            status_code=400,
            detail=(
                "Thumbnail generation is only supported for image assets. "
                f"Asset type '{asset.content_type}' is not supported."
            ),
        )

    # ---- ONLY NOW create journal + job ----
    journal = MutationJournal(
        intent_type="GenerateAssetThumbnail",
        target_type="asset",
        target_id=asset.id,
        before_state={"thumbnail_key": asset.thumbnail_key},
        after_state={"thumbnail_key": None},
        issued_by_user_id=user.id,
        reason=reason,
    )

    db.add(journal)
    db.commit()
    db.refresh(journal)

    job = crud.create_job(
        db,
        mutation_id=journal.id,
        job_type="THUMBNAIL_GENERATION",
        target_type="asset",
        target_id=asset.id,
    )

    return {
        "status": "accepted",
        "jobId": job.id,
        "jobState": job.state,
    }


