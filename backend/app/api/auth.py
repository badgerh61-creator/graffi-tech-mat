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

router = APIRouter()


# -------------------------
# REGISTER
# -------------------------

@router.post("/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(400, "Email already registered")

    hashed = security.hash_password(user_in.password)
    return crud.create_user(db, user_in, hashed)


# -------------------------
# LOGIN
# -------------------------

@router.post("/login", response_model=schemas.TokenPair)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")

    access_token = security.create_access_token(user.id)

    refresh_token = security.generate_refresh_token()
    create_refresh_token(
        db,
        user_id=user.id,
        token=refresh_token,
        expires_at=security.refresh_token_expiry(),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


# -------------------------
# REFRESH
# -------------------------

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    refresh_token: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    rt = get_refresh_token(db, refresh_token.refresh_token)
    if not rt or rt.expires_at < datetime.utcnow():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")

    # 🔁 ROTATION
    revoke_refresh_token(db, rt)

    new_access = security.create_access_token(rt.user_id)

    new_refresh = security.generate_refresh_token()
    create_refresh_token(
        db,
        user_id=rt.user_id,
        token=new_refresh,
        expires_at=security.refresh_token_expiry(),
    )

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
    }


# -------------------------
# LOGOUT
# -------------------------

@router.post("/logout")
def logout(
    refresh_token: schemas.RefreshTokenRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    rt = get_refresh_token(db, refresh_token.refresh_token)
    if rt:
        revoke_refresh_token(db, rt)
    return {"detail": "Logged out"}

