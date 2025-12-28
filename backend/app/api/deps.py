# backend/app/api/deps.py

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import oauth2_scheme, decode_access_token
from app import crud
from app.models.user import User


# =========================
# AUTH
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Base authentication dependency.
    Validates access token and returns active user.
    """
    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = crud.get_user_by_id(db, user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


# =========================
# SAFE GLOBAL GUARDS
# =========================

def require_viewer(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Any authenticated user.
    Viewer is the lowest permission.
    """
    return current_user


def require_editor(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Editor-level *intent* guard.

    ⚠️ Does NOT enforce model permissions.
    Real enforcement happens via:
    - crud.require_model_role(...)
    - crud.require_owner(...)
    """
    return current_user


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Global admin-only access.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user

