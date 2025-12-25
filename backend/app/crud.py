from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta

from app.schemas import ModelCreate, AssetCreate, UserCreate
from app.models.user import User
from app.models.asset import Asset, AssetStatus
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
# ASSETS (PHASE 10 STATE MACHINE)
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
        status=AssetStatus.created,
        status_updated_at=datetime.utcnow(),
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
# ASSET STATE TRANSITIONS
# =========================

ALLOWED_TRANSITIONS = {
    AssetStatus.created: {AssetStatus.uploading, AssetStatus.failed},
    AssetStatus.uploading: {AssetStatus.uploaded, AssetStatus.failed},
    AssetStatus.uploaded: {AssetStatus.processing, AssetStatus.failed},
    AssetStatus.processing: {AssetStatus.ready, AssetStatus.failed},
    AssetStatus.ready: set(),
    AssetStatus.failed: set(),
}


def transition_asset_status(
    db: Session,
    *,
    asset: Asset,
    new_status: AssetStatus,
    error: str | None = None,
):
    if new_status not in ALLOWED_TRANSITIONS[asset.status]:
        raise ValueError(
            f"Illegal asset transition: {asset.status} → {new_status}"
        )

    asset.status = new_status
    asset.status_updated_at = datetime.utcnow()

    if new_status == AssetStatus.failed:
        asset.processing_error = error
    else:
        asset.processing_error = None

    db.commit()
    db.refresh(asset)
    return asset


# =========================
# MAINTENANCE / RECOVERY
# =========================

def list_stuck_assets(
    db: Session,
    *,
    older_than_minutes: int = 10,
):
    cutoff = datetime.utcnow() - timedelta(minutes=older_than_minutes)

    return (
        db.query(Asset)
        .filter(
            Asset.status.in_(
                [AssetStatus.uploading, AssetStatus.processing]
            ),
            Asset.status_updated_at < cutoff,
        )
        .all()
    )


def list_failed_assets(db: Session):
    return (
        db.query(Asset)
        .filter(Asset.status == AssetStatus.failed)
        .all()
    )


# =========================
# PHASE 10.3 — ADMIN RECOVERY
# =========================

def admin_retry_asset(db: Session, *, asset: Asset):
    """
    Admin-triggered retry.
    Only allowed from failed state.
    """
    if asset.status != AssetStatus.failed:
        raise ValueError("Only failed assets can be retried")

    asset.status = AssetStatus.uploaded
    asset.processing_error = None
    asset.status_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(asset)
    return asset


def admin_force_fail_asset(
    db: Session,
    *,
    asset: Asset,
    reason: str,
):
    """
    Admin-forced permanent failure.
    """
    asset.status = AssetStatus.failed
    asset.processing_error = reason
    asset.status_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(asset)
    return asset

