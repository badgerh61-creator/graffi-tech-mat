# backend/app/api/mutations.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.models.mutation_journal import MutationJournal
from app.crud import require_model_role
from app.services.mutations.rename_asset import RenameAssetAdapter

router = APIRouter(prefix="/mutations", tags=["mutations"])


@router.post("/rename-asset")
def rename_asset(
    *,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    payload: dict,
):
    # ---- 1. Validate payload ----
    target_id = payload.get("targetId")
    previous_name = payload.get("previousName")
    next_name = payload.get("nextName")
    reason = payload.get("reason")

    if not target_id or not previous_name or not next_name:
        raise HTTPException(status_code=400, detail="Invalid payload")

    # ---- 2. Load asset ----
    asset = db.query(Asset).filter(Asset.id == target_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    # ---- 3. Load model + permission gate ----
    model = db.query(ModelRecord).filter(ModelRecord.id == asset.model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    require_model_role(
        db,
        user=user,
        model=model,
        min_role="editor",
    )

    # ---- 4. Stale-state guard ----
    if asset.filename != previous_name:
        raise HTTPException(
            status_code=409,
            detail="Asset name out of date. Refresh required.",
        )

    # ---- 5. Prepare journal ----
    journal = MutationJournal(
        intent_type="RenameAsset",
        target_type="asset",
        target_id=asset.id,
        before_state={"filename": previous_name},
        after_state={"filename": next_name},
        issued_by_user_id=user.id,
        reason=reason,
    )

    # ---- 6. Atomic mutation + journal ----
    try:
        RenameAssetAdapter.execute(
            db,
            asset=asset,
            next_name=next_name,
        )
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

