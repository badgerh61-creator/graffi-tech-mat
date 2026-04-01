from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from app.models.user import User
from app.models.model import ModelRecord
from app.models.model_permission import ModelPermission
from app.models.model_invite import ModelInvite
from app.models.organization_member import OrganizationMember
from app.services.ownership import get_model_owner

ROLE_ORDER = {
    "viewer": 1,
    "editor": 2,
    "owner": 3,
    "admin": 4,
}


# =====================================================
# MODEL ACCESS QUERIES (IMPLEMENTED)
# =====================================================

def get_models_accessible_to_user(db: Session, user_id: int):
    """
    Return all models the user can access, with resolved role.

    MUST ALWAYS return a list.
    Empty list means: user has access to zero models.
    """
    rows = (
        db.query(ModelRecord, ModelPermission.role)
        .join(
            ModelPermission,
            ModelPermission.model_id == ModelRecord.id,
        )
        .filter(ModelPermission.user_id == user_id)
        .all()
    )
    return rows or []


# =====================================================
# CREATE MODEL (🔥 FIXED)
# =====================================================

def create_model(db: Session, model_in, *, owner_id: int):
    """
    Create a model and assign owner permission.
    """

    model = ModelRecord(
        name=model_in.name,
        description=getattr(model_in, "description", None),
        owner_id=owner_id,
        created_at=datetime.utcnow(),
    )

    db.add(model)
    db.flush()  # ensures model.id is available

    # 🔥 CRITICAL: give creator ownership
    permission = ModelPermission(
        model_id=model.id,
        user_id=owner_id,
        role="owner",
    )

    db.add(permission)

    db.commit()
    db.refresh(model)

    return model


# =====================================================
# BASIC HELPERS (SAFE IMPLEMENTATIONS)
# =====================================================

def get_model_by_id(db: Session, model_id: int):
    return db.query(ModelRecord).filter(ModelRecord.id == model_id).first()


def require_owner(db: Session, *, user: User, model: ModelRecord):
    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
        )
        .first()
    )

    if not perm or perm.role not in ("owner", "admin"):
        raise Exception("Owner access required")

    return True


def require_model_role(db: Session, *, user: User, model: ModelRecord, min_role: str):
    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
        )
        .first()
    )

    if not perm:
        raise Exception("No access to model")

    if ROLE_ORDER.get(perm.role, 0) < ROLE_ORDER.get(min_role, 0):
        raise Exception("Insufficient role")

    return True


def resolve_user_role_for_model(db: Session, *, model: ModelRecord, user: User) -> str:
    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
        )
        .first()
    )

    return perm.role if perm else "viewer"


def get_model_if_accessible(db: Session, *, model_id: int, user_id: int):
    row = (
        db.query(ModelRecord)
        .join(ModelPermission, ModelPermission.model_id == ModelRecord.id)
        .filter(
            ModelRecord.id == model_id,
            ModelPermission.user_id == user_id,
        )
        .first()
    )

    return row


# =====================================================
# INVITES (SAFE MINIMAL IMPLEMENTATION)
# =====================================================

def get_invite_by_token(db: Session, token: str):
    return db.query(ModelInvite).filter(ModelInvite.token == token).first()


def create_model_invite(db: Session, *, model: ModelRecord, email: str, role: str):
    invite = ModelInvite(
        model_id=model.id,
        email=email,
        role=role,
        token=secrets.token_urlsafe(32),
        created_at=datetime.utcnow(),
    )

    db.add(invite)
    db.commit()
    db.refresh(invite)

    return invite


def accept_model_invite(db: Session, *, invite: ModelInvite, user: User):
    permission = ModelPermission(
        model_id=invite.model_id,
        user_id=user.id,
        role=invite.role,
    )

    db.add(permission)
    db.delete(invite)

    db.commit()

    return permission
