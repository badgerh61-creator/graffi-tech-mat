# backend/app/api/admin.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_admin, get_current_user
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app import crud

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


# =========================
# USERS
# =========================

@router.get("/users", response_model=list[dict])
def list_users(
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    users = db.query(User).order_by(User.id).all()

    return [
        {
            "id": u.id,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at,
        }
        for u in users
    ]


@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin cannot deactivate themselves",
        )

    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = False

    # 🔒 revoke all refresh tokens
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked.is_(False),
    ).update({RefreshToken.revoked: True})

    db.commit()

    return {"detail": "User deactivated and sessions revoked"}


@router.post("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = True
    db.commit()

    return {"detail": "User activated"}


# =========================
# SESSIONS
# =========================

@router.post("/users/{user_id}/revoke-sessions")
def revoke_user_sessions(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    count = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked.is_(False),
        )
        .update({RefreshToken.revoked: True})
    )

    db.commit()

    return {
        "detail": "Sessions revoked",
        "revoked_count": count,
    }

