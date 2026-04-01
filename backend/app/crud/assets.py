# backend/app/crud/assets.py

from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import AssetCreate
from app.models.asset import Asset, AssetStatus


def create_asset(
    db: Session,
    asset_in: AssetCreate,
    *,
    model_id: int,
    user_id: int,
):
    """
    Phase I.2 invariant:
    - Asset visibility is metadata-only
    - Initialized here
    - Never mutated via CRUD
    """

    asset = Asset(
        model_id=model_id,
        filename=asset_in.filename,
        s3_key=asset_in.s3_key,
        content_type=asset_in.content_type,
        status=AssetStatus.processing,
        created_at=datetime.utcnow(),
        is_visible=True,  # ✅ Phase I.2 default
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset
    
    
def transition_asset_status(db: Session, *, asset: Asset, new_status: AssetStatus, error: str | None = None):
    """
    Simple status transition helper.
    """

    asset.status = new_status

    if error:
        # only if your model has an error field
        if hasattr(asset, "error"):
            asset.error = error

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset
