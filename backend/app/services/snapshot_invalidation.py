from fastapi import HTTPException, status
from datetime import datetime

from app.models.rendered_snapshot import RenderedSnapshot as Snapshot


def invalidate_snapshot(db, *, snapshot, user):
    """
    Legacy snapshot invalidation (Phase I.x compatibility).

    Contract:
    - Snapshot must exist
    - Only COMPLETED snapshots can be invalidated
    - Invalid state ⇒ 409 (NOT 404)
    """

    if snapshot is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Snapshot not found")

    if snapshot.status != "completed":
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Only completed snapshots can be invalidated",
        )

    snapshot.status = "obsolete"
    snapshot.invalidated_at = datetime.utcnow()

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot

