from sqlalchemy.orm import Session
from . import models, schemas

def create_model(db: Session, model_in: schemas.ModelCreate):
    m = models.ModelRecord(name=model_in.name, description=model_in.description)
    db.add(m); db.commit(); db.refresh(m); return m

def get_model(db: Session, model_id: int):
    return db.query(models.ModelRecord).filter(models.ModelRecord.id == model_id).first()

def list_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ModelRecord).offset(skip).limit(limit).all()

def create_asset(db: Session, asset_in: schemas.AssetCreate, model_id: int | None = None):
    a = models.Asset(
        filename=asset_in.filename,
        content_type=asset_in.content_type,
        size=asset_in.size,
        s3_key=asset_in.s3_key,
        model_id=model_id,
        processed=False,
    )
    db.add(a); db.commit(); db.refresh(a); return a

def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

def list_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asset).offset(skip).limit(limit).all()

def mark_asset_processed(db: Session, asset, thumbnail_key: str | None = None):
    asset.processed = True
    if thumbnail_key:
        asset.thumbnail_key = thumbnail_key
    db.add(asset); db.commit(); db.refresh(asset); return asset

# User crud
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate, hashed_password: str):
    u = models.User(email=user_in.email, hashed_password=hashed_password)
    db.add(u); db.commit(); db.refresh(u); return u
