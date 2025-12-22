# backend/app/crud.py

from sqlalchemy.orm import Session

from app.schemas import ModelCreate, AssetCreate, UserCreate
from app.models.user import User
from app.models.asset import Asset
from app.models.model import ModelRecord


# =========================
# USERS
# =========================

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    user_in: UserCreate,
    hashed_password: str,
):
    user = User(
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# =========================
# MODELS
# =========================

def create_model(
    db: Session,
    model_in: ModelCreate,
    owner_id: int,
):
    model = ModelRecord(
        name=model_in.name,
        description=model_in.description,
        owner_id=owner_id,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def get_model(db: Session, model_id: int):
    return db.query(ModelRecord).filter(ModelRecord.id == model_id).first()


def get_models_for_user(db: Session, user_id: int):
    return db.query(ModelRecord).filter(ModelRecord.owner_id == user_id).all()


# =========================
# ASSETS
# =========================

def create_asset(
    db: Session,
    asset_in: AssetCreate,
    model_id: int | None = None,
):
    asset = Asset(
        filename=asset_in.filename,
        content_type=asset_in.content_type,
        size=asset_in.size,
        s3_key=asset_in.s3_key,
        model_id=model_id,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def get_asset(db: Session, asset_id: int):
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Asset).offset(skip).limit(limit).all()

