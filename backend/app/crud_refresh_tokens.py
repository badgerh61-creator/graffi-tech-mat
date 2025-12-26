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

    Guarantees:
    - ONE active refresh token per user
    - Transaction-safe
    - No flush-time mutations
    """

    # 1️⃣ Revoke all existing active tokens (bulk update only)
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked.is_(False),
    ).update(
        {RefreshToken.revoked: True},
        synchronize_session=False,
    )

    # 2️⃣ Create new refresh token
    rt = RefreshToken(
        user_id=user_id,
        token_hash=hash_refresh_token(token),
        expires_at=expires_at,
        revoked=False,
    )

    db.add(rt)

    # 3️⃣ Single commit
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
    Explicit logout / rotation revoke.
    SAFE: mutates only a persistent object.
    """
    rt.revoked = True
    db.commit()

