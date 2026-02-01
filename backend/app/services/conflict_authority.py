from app.models.conflict import SnapshotConflict
from app.services.conflict_detector import detect_conflict


def has_any_conflict(*, db, snapshot, user):
    """
    Phase U.4+ — Conflict Authority Aggregator

    A draft is conflicted if:
    - U.3 structural conflict exists
    - OR an explicit SnapshotConflict row exists
    """

    # 1️⃣ Structural (Phase U.3 — frozen)
    structural = detect_conflict(
        db=db,
        snapshot=snapshot,
        user=user,
    )
    if structural.is_conflicted:
        return structural

    # 2️⃣ Explicit (Phase U.4)
    explicit = (
        db.query(SnapshotConflict)
        .filter(SnapshotConflict.snapshot_id == snapshot.id)
        .first()
    )
    if explicit:
        return type(structural)(
            is_conflicted=True,
            reason="explicit_conflict",
        )

    return structural

