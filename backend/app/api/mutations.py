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

    require_model_role(db, user=user, model=model, min_role="editor")

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

    require_model_role(db, user=user, model=model, min_role="editor")

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
            next_is_visible=next_value,  # ✅ FIXED
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

