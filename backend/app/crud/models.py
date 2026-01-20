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
# STUBS — REQUIRED FOR IMPORT SAFETY
# =====================================================

def create_model(db: Session, model_in, *, owner_id: int):
    raise NotImplementedError("create_model not implemented yet")


def get_model_by_id(db: Session, model_id: int):
    raise NotImplementedError("get_model_by_id not implemented yet")


def require_owner(db: Session, *, user: User, model: ModelRecord):
    raise NotImplementedError("require_owner not implemented yet")


def require_model_role(db: Session, *, user: User, model: ModelRecord, min_role: str):
    raise NotImplementedError("require_model_role not implemented yet")


def resolve_user_role_for_model(db: Session, *, model: ModelRecord, user: User) -> str:
    raise NotImplementedError("resolve_user_role_for_model not implemented yet")


def get_model_if_accessible(db: Session, *, model_id: int, user_id: int):
    raise NotImplementedError("get_model_if_accessible not implemented yet")


def get_invite_by_token(db: Session, token: str):
    raise NotImplementedError("get_invite_by_token not implemented yet")


def create_model_invite(db: Session, *, model: ModelRecord, email: str, role: str):
    raise NotImplementedError("create_model_invite not implemented yet")


def accept_model_invite(db: Session, *, invite: ModelInvite, user: User):
    raise NotImplementedError("accept_model_invite not implemented yet")

