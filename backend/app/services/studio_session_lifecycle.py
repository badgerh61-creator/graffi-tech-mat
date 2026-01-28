from datetime import datetime, timedelta

from app.models.studio_session import StudioSession


DEFAULT_SESSION_TTL_SECONDS = 900  # 15 minutes


def start_session(
    *,
    db,
    user,
    project_id: int,
    snapshot_id: int | None = None,
    ttl_seconds: int = DEFAULT_SESSION_TTL_SECONDS,
):
    expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    session = StudioSession(
        user_id=user.id,
        project_id=project_id,
        snapshot_id=snapshot_id,
        expires_at=expires_at,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def end_session(
    *,
    db,
    session: StudioSession,
):
    db.delete(session)
    db.commit()

