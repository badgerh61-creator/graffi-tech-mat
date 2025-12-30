# =========================================
# Graffi-Tech-Mat — CRUD (Phase 4.6 FINAL)
# =========================================

from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from app.schemas import ModelCreate, AssetCreate, UserCreate
from app.models.user import User
from app.models.asset import Asset, AssetStatus
from app.models.model import ModelRecord
from app.models.model_permission import ModelPermission
from app.models.model_invite import ModelInvite
from app.models.organization_member import OrganizationMember
from app.services.ownership import get_model_owner


# =========================
# USERS
# =========================

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# =========================
# ASSETS
# =========================

def create_asset(db: Session, asset_in: AssetCreate, *, model_id: int, user_id: int):
    asset = Asset(
        model_id=model_id,
        filename=asset_in.filename,
        s3_key=asset_in.s3_key,
        content_type=asset_in.content_type,
        status=AssetStatus.processing,
        uploaded_by_id=user_id,
        created_at=datetime.utcnow(),
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


# =========================
# MODELS
# =========================

def create_model(db: Session, model_in: ModelCreate, *, owner_id: int):
    model = ModelRecord(
        name=model_in.name,
        description=model_in.description,
        owner_id=owner_id,
        created_at=datetime.utcnow(),
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def get_model_by_id(db: Session, model_id: int):
    return db.query(ModelRecord).filter(ModelRecord.id == model_id).first()


def require_owner(db: Session, *, user: User, model: ModelRecord):
    if user.is_admin:
        return

    owner = get_model_owner(db, model)
    if owner["type"] == "user" and owner["id"] == user.id:
        return

    raise PermissionError("Owner access required")


def resolve_user_role_for_model(db: Session, *, model: ModelRecord, user: User) -> str:
    if user.is_admin:
        return "admin"

    if model.owner_id == user.id:
        return "owner"

    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
        )
        .first()
    )
    if perm:
        return perm.role

    owner = get_model_owner(db, model)
    if owner["type"] == "organization":
        member = (
            db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == owner["id"],
                OrganizationMember.user_id == user.id,
            )
            .first()
        )
        if member:
            return "viewer"

    return "viewer"


def get_models_accessible_to_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    results = []

    for model in db.query(ModelRecord).all():
        owner = get_model_owner(db, model)

        allowed = (
            (owner["type"] == "user" and owner["id"] == user_id)
            or db.query(ModelPermission)
              .filter(
                  ModelPermission.model_id == model.id,
                  ModelPermission.user_id == user_id,
              )
              .first()
            or (
                owner["type"] == "organization"
                and db.query(OrganizationMember)
                .filter(
                    OrganizationMember.organization_id == owner["id"],
                    OrganizationMember.user_id == user_id,
                )
                .first()
            )
        )

        if allowed:
            results.append((model, resolve_user_role_for_model(db, model=model, user=user)))

    return sorted(results, key=lambda r: r[0].created_at, reverse=True)


def get_model_if_accessible(db: Session, *, model_id: int, user_id: int):
    model = get_model_by_id(db, model_id)
    if not model:
        return None

    owner = get_model_owner(db, model)

    if owner["type"] == "user" and owner["id"] == user_id:
        return model

    if db.query(ModelPermission).filter(
        ModelPermission.model_id == model.id,
        ModelPermission.user_id == user_id,
    ).first():
        return model

    if owner["type"] == "organization":
        if db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == owner["id"],
            OrganizationMember.user_id == user_id,
        ).first():
            return model

    return None


# =========================
# INVITES
# =========================

def get_invite_by_token(db: Session, token: str):
    return db.query(ModelInvite).filter(ModelInvite.token == token).first()


def create_model_invite(db: Session, *, model, email: str, role: str):
    invite = ModelInvite(
        model_id=model.id,
        email=email,
        role=role,
        token=secrets.token_urlsafe(32),
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite


def accept_model_invite(db: Session, *, invite: ModelInvite, user: User):
    db.add(
        ModelPermission(
            model_id=invite.model_id,
            user_id=user.id,
            role=invite.role,
        )
    )
    db.delete(invite)
    db.commit()

