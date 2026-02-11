from fastapi import HTTPException

from app.models.read_view import ReadView
from app.models.session import StudioSession
from app.models.conflict import SnapshotConflict
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
    """
    Phase U.5 — Read View Guard (AUTHORITATIVE)

    Rules:
    - Conflicts dominate (never emit 403)
    - Owners are NEVER blocked by read views
    - Non-owners with active read views get 403
    """

    # 1️⃣ Conflict dominates
    conflict = (
        db.query(SnapshotConflict)
        .filter(SnapshotConflict.snapshot_id == snapshot.id)
        .first()
    )
    if conflict:
        return  # let conflict guard raise 409

    # 2️⃣ Owners are never blocked
    if snapshot.owner_user_id == user.id:
        return

    # 3️⃣ Non-owner + read view = 403
    if has_active_read_view(
        db=db,
        snapshot=snapshot,
        user=user,
    ):
        raise HTTPException(403, "Read-only view")

