# backend/app/crud.py

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
from app.models.organization_member import OrganizationMember
from app.services.ownership import get_model_owner


# =========================
# MODELS — ACCESS
# =========================

def get_models_accessible_to_user(db: Session, user_id: int):
    """
    Returns all models accessible to the user via:
    - direct ownership
    - collaboration
    - organization membership
    """

    models = (
        db.query(ModelRecord)
        .outerjoin(ModelPermission, ModelPermission.model_id == ModelRecord.id)
        .distinct()
        .all()
    )

    accessible = []

    for model in models:
        owner = get_model_owner(db, model)

        # User-owned
        if owner["type"] == "user" and owner["id"] == user_id:
            accessible.append(model)
            continue

        # Explicit permission
        perm = (
            db.query(ModelPermission)
            .filter(
                ModelPermission.model_id == model.id,
                ModelPermission.user_id == user_id,
            )
            .first()
        )
        if perm:
            accessible.append(model)
            continue

        # Organization-owned
        if owner["type"] == "organization":
            member = (
                db.query(OrganizationMember)
                .filter(
                    OrganizationMember.organization_id == owner["id"],
                    OrganizationMember.user_id == user_id,
                )
                .first()
            )
            if member:
                accessible.append(model)

    return sorted(accessible, key=lambda m: m.created_at, reverse=True)


def get_model_if_accessible(db: Session, *, model_id: int, user_id: int):
    model = db.query(ModelRecord).filter(ModelRecord.id == model_id).first()
    if not model:
        return None

    owner = get_model_owner(db, model)

    if owner["type"] == "user" and owner["id"] == user_id:
        return model

    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user_id,
        )
        .first()
    )
    if perm:
        return model

    if owner["type"] == "organization":
        member = (
            db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == owner["id"],
                OrganizationMember.user_id == user_id,
            )
            .first()
        )
        if member:
            return model

    return None


# =========================
# ROLE ENFORCEMENT
# =========================

ROLE_ORDER = {
    "viewer": 1,
    "editor": 2,
    "owner": 3,
    "admin": 4,
}


ORG_ROLE_MAP = {
    "member": "viewer",
    "admin": "editor",
    "owner": "owner",
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

    owner = get_model_owner(db, model)

    # User-owned
    if owner["type"] == "user" and owner["id"] == user.id:
        return

    # Org-owned
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
            mapped_role = ORG_ROLE_MAP.get(member.role, "viewer")
            if ROLE_ORDER[mapped_role] >= ROLE_ORDER[min_role]:
                return

    # Explicit permission
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


def require_owner(db: Session, *, user: User, model: ModelRecord):
    if user.is_admin:
        return

    owner = get_model_owner(db, model)

    if owner["type"] == "user" and owner["id"] == user.id:
        return

    if owner["type"] == "organization":
        member = (
            db.query(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == owner["id"],
                OrganizationMember.user_id == user.id,
                OrganizationMember.role == "owner",
            )
            .first()
        )
        if member:
            return

    raise PermissionError("Owner access required")

