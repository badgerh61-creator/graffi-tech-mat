# =========================================
# Graffi-Tech-Mat — Auth & RBAC (Phase 4.6 FINAL)
# Phase H1 FIX — JWT alignment
# =========================================

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import oauth2_scheme, decode_access_token
from app import crud
from app.models.user import User


# =====================================================
# CANONICAL USER RESOLUTION
# =====================================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Canonical authentication resolver.

    RULES:
    - JWT proves identity only (sub)
    - Database is source of truth
    - No role or permission assumptions from token
    """

    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = crud.get_user_by_id(db, int(user_id))

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


# =====================================================
# ROLE GUARDS (GLOBAL)
# =====================================================
def require_viewer(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Any authenticated, active user.
    """
    return current_user


def require_editor(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Global editor/admin guard.
    Editors may create models and edit content.
    """

    if current_user.is_admin:
        return current_user

    # IMPORTANT:
    # Role is resolved from DB, not JWT
    if current_user.role != "editor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return current_user


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Admin-only guard.
    """

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return current_user

