# backend/app/api/model_deps.py
# =========================================
# Graffi-Tech-Mat — Model Permission Guards
# Phase 5 Ready
# =========================================

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app import crud
from app.models.user import User
from app.models.model_permission import ModelPermission


def require_model_viewer(
    model_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    model = crud.get_model_if_accessible(db, model_id=model_id, user_id=user.id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found or no access",
        )
    return model


def require_model_editor(
    model_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    model = require_model_viewer(model_id, db, user)

    if user.is_admin:
        return model

    perm = (
        db.query(ModelPermission)
        .filter(
            ModelPermission.model_id == model.id,
            ModelPermission.user_id == user.id,
            ModelPermission.role.in_(["editor", "owner"]),
        )
        .first()
    )

    owner = crud.get_model_owner(db, model)

    if owner["type"] == "user" and owner["id"] == user.id:
        return model

    if perm:
        return model

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Editor permissions required",
    )


def require_model_owner(
    model_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    model = require_model_viewer(model_id, db, user)

    owner = crud.get_model_owner(db, model)

    if user.is_admin:
        return model

    if owner["type"] == "user" and owner["id"] == user.id:
        return model

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Owner permissions required",
    )

