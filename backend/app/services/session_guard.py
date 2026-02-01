from fastapi import HTTPException
from datetime import datetime

from app.models.session import StudioSession


def require_active_session(*, db, user, project_id):
    now = datetime.utcnow()

    session = (
        db.query(StudioSession)
        .filter(
            StudioSession.user_id == user.id,
            StudioSession.project_id == project_id,
            StudioSession.expires_at > now,
        )
        .order_by(StudioSession.expires_at.desc())
        .first()
    )

    if not session:
        raise HTTPException(403, "No active studio session")

    return session

