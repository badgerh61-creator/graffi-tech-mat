from datetime import datetime
from fastapi import HTTPException

from app.models.read_view import ReadView
from app.models.session import StudioSession


def has_active_read_view(*, db, snapshot, user) -> bool:
    now = datetime.utcnow()

    return (
        db.query(ReadView)
        .join(StudioSession, ReadView.session_id == StudioSession.id)
        .filter(
            ReadView.snapshot_id == snapshot.id,
            ReadView.user_id == user.id,
            StudioSession.expires_at > now,
        )
        .count()
        > 0
    )


def reject_mutation_from_read_view(*, db, snapshot, user):
    if has_active_read_view(
        db=db,
        snapshot=snapshot,
        user=user,
    ):
        raise HTTPException(403, "Read-only view")

