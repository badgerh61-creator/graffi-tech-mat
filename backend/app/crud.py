# =========================================
# Graffi-Tech-Mat — CRUD (Phase 4.6 FINAL)
# Phase I.3 compliant
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
        uploaded_by_id=user_id,
        created_at=datetime.utcnow(),
        is_visible=True,  # ✅ Phase I.2 default
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


# =========================
# MODELS
# =========================

def create_model(
    db: Session,
    model_in: ModelCreate,
    *,
    owner_id: int,
):
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
    return (
        db.query(ModelRecord)
        .filter(ModelRecord.id == model_id)
        .first()
    )


def require_owner(
    db: Session,
    *,
    user: User,
    model: ModelRecord,
):
    if user.is_admin:
        return

    owner = get_model_owner(db, model)

    if owner["type"] == "user" and owner["id"] == user.id:
        return

    raise PermissionError("Owner access required")


# =========================
# 🆕 PHASE I — ROLE ENFORCEMENT (MODEL)
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
    """
    Enforce minimum role on a model.
    Used by Phase I mutation intents.
    """

    # Admin bypass
    if user.is_admin:
        return

    owner = get_model_owner(db, model)

    # ---- User-owned model ----
    if owner["type"] == "user" and owner["id"] == user.id:
        return

    # ---- Organization-owned model ----
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
            org_role_map = {
                "member": "viewer",
                "admin": "editor",
                "owner": "owner",
            }
            mapped = org_role_map.get(member.role, "viewer")
            if ROLE_ORDER[mapped] >= ROLE_ORDER[min_role]:
                return

    # ---- Explicit collaborator permission ----
    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
        )
        .first()
    )
    if perm and ROLE_ORDER[perm.role] >= ROLE_ORDER[min_role]:
        return

    raise PermissionError(f"Requires {min_role} role or higher")


def resolve_user_role_for_model(
    db: Session,
    *,
    model: ModelRecord,
    user: User,
) -> str:
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


# =========================
# PROJECT — ROLE ENFORCEMENT (PHASE I.3)
# =========================

def require_project_role(
    db: Session,
    *,
    user: User,
    project,
    min_role: str,
):
    """
    Phase I.3:
    Simple project ownership enforcement.
    Expandable later to org/project roles.
    """

    if user.is_admin:
        return

    if project.owner_id == user.id:
        return

    raise PermissionError("Insufficient project permissions")


# =========================
# ACCESS RESOLUTION (FIXED)
# =========================

def get_models_accessible_to_user(db: Session, user_id: int):
    """
    Canonical access resolver.
    FIXED: Forces eager materialization to prevent
    sqlite 'closed database' errors.
    """

    user = get_user_by_id(db, user_id)
    results = []

    models = list(db.query(ModelRecord).all())

    for model in models:
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
            role = resolve_user_role_for_model(
                db,
                model=model,
                user=user,
            )
            results.append((model, role))

    return sorted(
        results,
        key=lambda r: r[0].created_at,
        reverse=True,
    )


def get_model_if_accessible(
    db: Session,
    *,
    model_id: int,
    user_id: int,
):
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
    return (
        db.query(ModelInvite)
        .filter(ModelInvite.token == token)
        .first()
    )


def create_model_invite(
    db: Session,
    *,
    model: ModelRecord,
    email: str,
    role: str,
):
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


def accept_model_invite(
    db: Session,
    *,
    invite: ModelInvite,
    user: User,
):
    db.add(
        ModelPermission(
            model_id=invite.model_id,
            user_id=user.id,
            role=invite.role,
        )
    )
    db.delete(invite)
    db.commit()


# =========================
# JOBS (PHASE I.6)
# =========================

from app.models.job import Job

def create_job(
    db: Session,
    *,
    mutation_id: int,
    job_type: str,
    target_type: str,
    target_id: int,
) -> Job:
    job = Job(
        mutation_id=mutation_id,
        job_type=job_type,
        target_type=target_type,
        target_id=target_id,
        state="CREATED",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

