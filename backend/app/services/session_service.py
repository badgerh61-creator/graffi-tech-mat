from datetime import datetime, timedelta

from app.models.session import StudioSession

def start_session(*, db, user, project_id, ttl_seconds=3600):
    session = StudioSession(
        user_id=user.id,
        project_id=project_id,
        expires_at=datetime.utcnow() + timedelta(seconds=ttl_seconds),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def end_session(*, db, session):
    db.delete(session)
    db.commit()

