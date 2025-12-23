from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from app import crud, schemas
from app.db.session import get_db
from app.core import security
from app.api.deps import get_current_user
from app.crud_refresh_tokens import (
    create_refresh_token,
    get_refresh_token,
    revoke_refresh_token,
)

router = APIRouter(tags=["auth"])


# =========================
# REGISTER
# =========================

@router.post("/register", response_model=schemas.UserRead)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed = security.hash_password(user_in.password)
    return crud.create_user(db, user_in, hashed)


# =========================
# LOGIN
# =========================

@router.post("/login", response_model=schemas.TokenPair)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)

    if not user or not security.verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # ✅ correct positional call
    access_token = security.create_access_token(user.id)

    refresh_token = security.generate_refresh_token()
    create_refresh_token(
        db,
        user_id=user.id,
        token=refresh_token,
        expires_at=security.refresh_token_expiry(),
    )

    return schemas.TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


# =========================
# REFRESH
# =========================

@router.post("/refresh", response_model=schemas.TokenPair)
def refresh_token(
    data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    rt = get_refresh_token(db, data.refresh_token)

    if not rt or rt.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # 🔁 rotate old token
    revoke_refresh_token(db, rt)

    new_access = security.create_access_token(rt.user_id)
    new_refresh = security.generate_refresh_token()

    create_refresh_token(
        db,
        user_id=rt.user_id,
        token=new_refresh,
        expires_at=security.refresh_token_expiry(),
    )

    return schemas.TokenPair(
        access_token=new_access,
        refresh_token=new_refresh,
    )


# =========================
# LOGOUT
# =========================

@router.post("/logout")
def logout(
    data: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    rt = get_refresh_token(db, data.refresh_token)
    if rt:
        revoke_refresh_token(db, rt)

    return {"detail": "Logged out"}


# =========================
# CURRENT USER (IDENTITY CHECK)
# =========================

@router.get("/me", response_model=schemas.UserRead)
def read_me(
    user=Depends(get_current_user),
):
    return user

