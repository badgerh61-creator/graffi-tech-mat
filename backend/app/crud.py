from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas import AssetCreate

def create_asset(db: Session, asset: AssetCreate):
    db_asset = Asset(
        id=asset.id,
        name=asset.name,
        type=asset.type,
        url=asset.url,
        thumbnail_url=asset.thumbnail_url,
        size=asset.size,
        meta=asset.meta or {}
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset
