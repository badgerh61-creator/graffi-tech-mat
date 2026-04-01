from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from minio.error import S3Error

from app.db.session import get_db
from app.api.deps import get_current_user
from app import crud
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.services import storage as s3
from app.core.config import settings  # 🔥 REQUIRED

router = APIRouter(prefix="/assets", tags=["assets"])

ASSET_URL_EXPIRES = 120


@router.get("/")
def list_assets(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    List all assets belonging to models the user can access
    """
    rows = crud.get_models_accessible_to_user(db, user.id)

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

    serialized = [
        {
            "id": a.id,
            "filename": a.filename,
            "model_id": a.model_id,
            "processed": True,
        }
        for a in assets
    ]

    return {
        "items": serialized,
        "total": len(serialized),
    }


@router.get("/{asset_id}/url")
def get_asset_url(
    asset_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Return a presigned URL if:
    - user has access
    - file EXISTS in storage (critical fix)
    """

    asset = (
        db.query(Asset)
        .join(ModelRecord)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    model = crud.get_model_if_accessible(
        db,
        model_id=asset.model_id,
        user_id=user.id,
    )

    if not model:
        raise HTTPException(status_code=403, detail="No access to asset")

    # 🔥 CRITICAL FIX — VERIFY FILE EXISTS (CORRECT CLIENT)
    try:
        s3.get_client().stat_object(
            settings.MINIO_BUCKET,
            asset.s3_key,
        )
    except S3Error:
        print(f"❌ Missing asset in storage: {asset.s3_key}")
        raise HTTPException(
            status_code=404,
            detail="Asset file missing in storage",
        )

    # ✅ ONLY generate URL if file exists
    url = s3.get_presigned_url(
        asset.s3_key,
        expires_seconds=ASSET_URL_EXPIRES,
    )

    return {
        "url": url,
        "expires_in": ASSET_URL_EXPIRES,
        "type": "glb" if asset.filename.lower().endswith(".glb") else "image",
    }
