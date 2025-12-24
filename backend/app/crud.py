from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta

from app.schemas import ModelCreate, AssetCreate, UserCreate
from app.models.user import User
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.models.model_permission import ModelPermission


# =========================
# USERS
# =========================

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def list_users(db: Session):
    return db.query(User).order_by(User.id).all()


def create_user(db: Session, user_in: UserCreate, hashed_password: str):
    user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role="viewer",
        is_admin=False,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def set_user_role(db: Session, user_id: int, role: str):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.role = role
    user.is_admin = role == "admin"

    db.commit()
    db.refresh(user)
    return user


# =========================
# MODELS
# =========================

def create_model(db: Session, model_in: ModelCreate, owner_id: int):
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


def get_models_accessible_to_user(db: Session, user_id: int):
    return (
        db.query(ModelRecord)
        .outerjoin(ModelPermission, ModelPermission.model_id == ModelRecord.id)
        .filter(
            or_(
                ModelRecord.owner_id == user_id,
                ModelPermission.user_id == user_id,
            )
        )
        .distinct()
        .order_by(ModelRecord.created_at.desc())
        .all()
    )


def get_model_if_accessible(db: Session, *, model_id: int, user_id: int):
    return (
        db.query(ModelRecord)
        .outerjoin(ModelPermission, ModelPermission.model_id == ModelRecord.id)
        .filter(
            ModelRecord.id == model_id,
            or_(
                ModelRecord.owner_id == user_id,
                ModelPermission.user_id == user_id,
            ),
        )
        .first()
    )


# =========================
# ASSETS (CORE)
# =========================

def create_asset(db: Session, asset_in: AssetCreate, model_id: int | None = None):
    asset = Asset(
        filename=asset_in.filename,
        content_type=asset_in.content_type,
        size=asset_in.size,
        s3_key=asset_in.s3_key,
        model_id=model_id,
        processed=False,
        processing_error=None,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, *, asset: Asset):
    db.delete(asset)
    db.commit()


# =========================
# PHASE 4.3 — RECOVERY HELPERS
# =========================

def list_unprocessed_assets(db: Session, older_than_minutes: int = 5):
    """
    Assets stuck in pending state beyond threshold.
    """
    cutoff = datetime.utcnow() - timedelta(minutes=older_than_minutes)
    return (
        db.query(Asset)
        .filter(
            Asset.processed.is_(False),
            Asset.created_at < cutoff,
        )
        .all()
    )


def list_failed_assets(db: Session):
    """
    Assets with explicit processing failures.
    """
    return (
        db.query(Asset)
        .filter(Asset.processing_error.isnot(None))
        .all()
    )


def mark_asset_failed(
    db: Session,
    *,
    asset: Asset,
    reason: str,
):
    asset.processing_error = reason
    asset.processed = False
    db.commit()
    db.refresh(asset)
    return asset


def mark_asset_processed(db: Session, *, asset: Asset):
    asset.processed = True
    asset.processing_error = None
    db.commit()
    db.refresh(asset)
    return asset


def cleanup_orphan_assets(
    db: Session,
    *,
    max_age_minutes: int = 60,
):
    """
    Deletes DB rows for assets that:
    - never processed
    - are old
    - safe to remove
    """
    cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)

    orphans = (
        db.query(Asset)
        .filter(
            Asset.processed.is_(False),
            Asset.created_at < cutoff,
        )
        .all()
    )

    for asset in orphans:
        db.delete(asset)

    db.commit()
    return len(orphans)

