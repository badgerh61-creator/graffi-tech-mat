from datetime import timedelta
from fastapi import HTTPException

from app.models.session import StudioSession
from app.services.clock import clock


def start_session(*, db, user, project_id, ttl_seconds=3600):
    session = StudioSession(
        user_id=user.id,
        project_id=project_id,
        expires_at=clock.now() + timedelta(seconds=ttl_seconds),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def end_session(*, db, session):
    db.delete(session)
    db.commit()


def require_active_session(*, session):
    """
    Kernel-level guard.
    Must raise if session is expired or invalid.
    """
    if session.expires_at <= clock.now():
        raise HTTPException(status_code=401, detail="Session expired")

    return session

