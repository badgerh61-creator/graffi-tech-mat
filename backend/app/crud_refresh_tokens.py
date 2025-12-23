# backend/app/crud_refresh_tokens.py

from sqlalchemy.orm import Session
from datetime import datetime

from app.models.refresh_token import RefreshToken
from app.core.security import hash_refresh_token


def create_refresh_token(
    db: Session,
    *,
    user_id: int,
    token: str,
    expires_at: datetime,
):
    """
    Create a refresh token for a user.

    IMPORTANT:
    - Revokes ALL existing active refresh tokens for this user
    - Guarantees ONE active refresh token per user
    """

    # 🔒 Revoke all existing active tokens for this user
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked.is_(False),
    ).update({RefreshToken.revoked: True})

    rt = RefreshToken(
        user_id=user_id,
        token_hash=hash_refresh_token(token),
        expires_at=expires_at,
        revoked=False,
    )

    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def get_refresh_token(db: Session, token: str):
    """
    Fetch a valid (non-revoked) refresh token by plaintext token.
    """
    token_hash = hash_refresh_token(token)

    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked.is_(False),
        )
        .first()
    )


def revoke_refresh_token(db: Session, rt: RefreshToken):
    """
    Revoke a refresh token explicitly (logout / rotation).
    """
    rt.revoked = True
    db.add(rt)
    db.commit()

