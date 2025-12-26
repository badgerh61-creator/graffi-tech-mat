from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import secrets

from app.schemas import ModelCreate, AssetCreate, UserCreate
from app.models.user import User
from app.models.asset import Asset, AssetStatus
from app.models.model import ModelRecord
from app.models.model_permission import ModelPermission
from app.models.model_invite import ModelInvite, InviteStatus


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
# ROLE ENFORCEMENT
# =========================

ROLE_ORDER = {
    "viewer": 1,
    "editor": 2,
    "owner": 3,
    "admin": 4,
}


def require_model_role(
    db: Session,
    *,
    user: User,
    model: ModelRecord,
    min_role: str,
):
    if user.is_admin:
        return

    if model.owner_id == user.id:
        return

    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
        )
        .first()
    )

    if not perm:
        raise PermissionError("No access to this model")

    if ROLE_ORDER.get(perm.role, 0) < ROLE_ORDER.get(min_role, 0):
        raise PermissionError(
            f"Requires {min_role} role or higher"
        )


def require_owner(
    db: Session,
    *,
    user: User,
    model: ModelRecord,
):
    if user.is_admin:
        return

    if model.owner_id != user.id:
        raise PermissionError("Owner access required")


# =========================
# INVITES
# =========================

def create_model_invite(
    db: Session,
    *,
    model: ModelRecord,
    email: str,
    role: str,
    invited_by_id: int,
):
    token = secrets.token_urlsafe(32)

    invite = ModelInvite(
        model_id=model.id,
        email=email.lower(),
        role=role,
        token=token,
        invited_by_id=invited_by_id,
        status=InviteStatus.pending,
    )

    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite


def get_invite_by_token(db: Session, token: str):
    return (
        db.query(ModelInvite)
        .filter(ModelInvite.token == token)
        .first()
    )


def accept_model_invite(
    db: Session,
    *,
    invite: ModelInvite,
    user: User,
):
    if invite.role == "owner":
        raise ValueError("Ownership transfer not supported")

    perm = ModelPermission(
        model_id=invite.model_id,
        user_id=user.id,
        role=invite.role,
    )
    db.add(perm)

    invite.status = InviteStatus.accepted
    invite.accepted_at = datetime.utcnow()

    db.commit()
    db.refresh(invite)
    return perm


def revoke_model_invite(db: Session, *, invite: ModelInvite):
    invite.status = InviteStatus.revoked
    db.commit()
    return invite


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
        status=AssetStatus.created,
        status_updated_at=datetime.utcnow(),
        processing_error=None,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def transition_asset_status(
    db: Session,
    *,
    asset: Asset,
    new_status: AssetStatus,
    error: str | None = None,
):
    ALLOWED_TRANSITIONS = {
        AssetStatus.created: {AssetStatus.uploading, AssetStatus.failed},
        AssetStatus.uploading: {AssetStatus.uploaded, AssetStatus.failed},
        AssetStatus.uploaded: {AssetStatus.processing, AssetStatus.failed},
        AssetStatus.processing: {AssetStatus.ready, AssetStatus.failed},
        AssetStatus.ready: set(),
        AssetStatus.failed: set(),
    }

    if new_status not in ALLOWED_TRANSITIONS[asset.status]:
        raise ValueError(
            f"Illegal asset transition: {asset.status} → {new_status}"
        )

    asset.status = new_status
    asset.status_updated_at = datetime.utcnow()
    asset.processing_error = error if new_status == AssetStatus.failed else None

    db.commit()
    db.refresh(asset)
    return asset

