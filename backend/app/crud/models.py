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

def create_model(db: Session, model_in, *, owner_id: int):
    ...

def get_model_by_id(db: Session, model_id: int):
    ...

def require_owner(db: Session, *, user: User, model: ModelRecord):
    ...

def require_model_role(db: Session, *, user: User, model: ModelRecord, min_role: str):
    ...

def resolve_user_role_for_model(db: Session, *, model: ModelRecord, user: User) -> str:
    ...

def get_models_accessible_to_user(db: Session, user_id: int):
    ...

def get_model_if_accessible(db: Session, *, model_id: int, user_id: int):
    ...

def get_invite_by_token(db: Session, token: str):
    ...

def create_model_invite(db: Session, *, model: ModelRecord, email: str, role: str):
    ...

def accept_model_invite(db: Session, *, invite: ModelInvite, user: User):
    ...

