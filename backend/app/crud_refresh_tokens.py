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
    rt = RefreshToken(
        user_id=user_id,
        token_hash=hash_refresh_token(token),
        expires_at=expires_at,
    )
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def get_refresh_token(db: Session, token: str):
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
    rt.revoked = True
    db.add(rt)
    db.commit()

