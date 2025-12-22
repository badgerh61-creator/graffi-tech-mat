from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
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
    return (
        db.query(Asset)
        .join(ModelRecord)
        .filter(ModelRecord.owner_id == user.id)
        .all()
    )


@router.get("/{asset_id}/url")
def get_asset_url(
    asset_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    asset = (
        db.query(Asset)
        .join(ModelRecord)
        .filter(
            Asset.id == asset_id,
            ModelRecord.owner_id == user.id,
        )
        .first()
    )

    if not asset:
        raise HTTPException(404, "Asset not found")

    return {
        "url": s3.get_presigned_url(
            asset.s3_key,
            expires_seconds=ASSET_URL_EXPIRES,
        ),
        "expires_in": ASSET_URL_EXPIRES,
        "type": "glb" if asset.filename.lower().endswith(".glb") else "image",
    }

