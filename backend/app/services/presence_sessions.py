from datetime import datetime, timedelta
from fastapi import HTTPException

from app.models.presence_session import PresenceSession
from app.services.audit import log_event


def start_session(*, db, user, project_id: int, ttl_seconds: int = 300):
    """
    Phase U.1 — Presence & Session Authority

    Starts (or renews) a session for a user on a project.
    """

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
    """
    Phase U.1 invariant:
    No kernel action without an active session.

    snapshot_id is accepted for Phase 5 compatibility
    and future conflict resolution.
    """

    session = (
        db.query(PresenceSession)
        .filter(
            PresenceSession.user_id == user.id,
            PresenceSession.project_id == project_id,
        )
        .first()
    )

    if not session or session.expires_at < datetime.utcnow():
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

