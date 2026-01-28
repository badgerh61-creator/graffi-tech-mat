from datetime import datetime, timedelta
from fastapi import HTTPException

from app.models.studio_session import StudioSession


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
    """

    session = (
        db.query(StudioSession)
        .filter(StudioSession.user_id == user.id)
        .filter(StudioSession.project_id == project_id)
        .first()
    )

    if not session:
        raise HTTPException(403, "No active session")

    if session.expires_at < datetime.utcnow():
        raise HTTPException(403, "Session expired")

    if snapshot_id is not None and session.snapshot_id != snapshot_id:
        raise HTTPException(403, "Session not valid for snapshot")

    return session

