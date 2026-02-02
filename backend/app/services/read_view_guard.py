from fastapi import HTTPException

from app.models.read_view import ReadView
from app.models.session import StudioSession
from app.services.clock import clock


def has_active_read_view(*, db, snapshot, user) -> bool:
    now = clock.now()

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
    # Phase U.5 — Read views block NON-OWNERS only
    if (
        getattr(snapshot, "locked_by_user_id", None) != user.id
        and has_active_read_view(db=db, snapshot=snapshot, user=user)
    ):
        raise HTTPException(403, "Read-only view")

