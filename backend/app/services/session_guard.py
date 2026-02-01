from fastapi import HTTPException
from datetime import datetime
from app.models.session import StudioSession

def require_active_session(*, db, user, project_id):
    session = (
        db.query(StudioSession)
        .filter(
            StudioSession.user_id == user.id,
            StudioSession.project_id == project_id,
        )
        .order_by(StudioSession.expires_at.desc())
        .first()
    )

    if not session or not session.is_active:
        raise HTTPException(403, "No active studio session")

