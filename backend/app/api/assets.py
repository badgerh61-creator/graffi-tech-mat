# backend/app/api/assets.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app import crud
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.services import storage as s3

router = APIRouter(prefix="/assets", tags=["assets"])

ASSET_URL_EXPIRES = 120


@router.get("/")
def list_assets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    List all assets belonging to models the user can access
    (Phase 4.6 compatible)
    """
    rows = crud.get_models_accessible_to_user(db, user.id)

    # rows = [(model, role), ...]
    model_ids = [model.id for model, _role in rows]

    if not model_ids:
        return {
            "items": [],
            "total": 0,
        }

    assets = (
        db.query(Asset)
        .filter(Asset.model_id.in_(model_ids))
        .all()
    )

    return {
        "items": assets,
        "total": len(assets),
    }


@router.get("/{asset_id}/url")
def get_asset_url(
    asset_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Return a presigned URL if the user can access the asset's model
    """
    asset = (
        db.query(Asset)
        .join(ModelRecord)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(404, "Asset not found")

    model = crud.get_model_if_accessible(
        db,
        model_id=asset.model_id,
        user_id=user.id,
    )

    if not model:
        raise HTTPException(403, "No access to asset")

    return {
        "url": s3.get_presigned_url(
            asset.s3_key,
            expires_seconds=ASSET_URL_EXPIRES,
        ),
        "expires_in": ASSET_URL_EXPIRES,
        "type": "glb" if asset.filename.lower().endswith(".glb") else "image",
    }

