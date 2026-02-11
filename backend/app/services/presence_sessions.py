from datetime import datetime as _real_datetime, timedelta
from fastapi import HTTPException

from app.models.presence_session import PresenceSession
from app.services.audit import log_event
from app.services.clock import clock


# 👇 must exist for monkeypatch
class _DatetimeProxy:
    @staticmethod
    def utcnow():
        # Always delegate to authoritative clock
        return clock.now()


# This is what tests monkeypatch
datetime = _DatetimeProxy


def start_session(*, db, user, project_id: int, ttl_seconds: int = 300):
    expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    session = PresenceSession(
        user_id=user.id,
        project_id=project_id,
        expires_at=expires_at,
    )

    db.add(session)

    log_event(
        db=db,
        user_id=user.id,
        action="session.started",
        resource_type="project",
        resource_id=project_id,
    )

    db.commit()
    db.refresh(session)
    return session


def require_active_session(
    *,
    db,
    user,
    project_id: int,
    snapshot_id: int | None = None,
):
    session = (
        db.query(PresenceSession)
        .filter(
            PresenceSession.user_id == user.id,
            PresenceSession.project_id == project_id,
        )
        .order_by(PresenceSession.expires_at.desc())
        .first()
    )

    now = datetime.utcnow()

    if not session or session.expires_at <= now:
        log_event(
            db=db,
            user_id=user.id,
            action="session.denied",
            resource_type="project",
            resource_id=project_id,
            extra={"snapshot_id": snapshot_id},
        )
        raise HTTPException(403, "No active session")

    return session

