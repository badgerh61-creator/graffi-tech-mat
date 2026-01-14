# backend/app/crud/invites.py

from sqlalchemy.orm import Session
import secrets

from app.models.user import User
from app.models.model import ModelRecord
from app.models.model_permission import ModelPermission
from app.models.model_invite import ModelInvite


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

