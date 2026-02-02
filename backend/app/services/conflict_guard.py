from fastapi import HTTPException
from app.models.conflict import SnapshotConflict

def require_no_conflict(*, db, snapshot, user):
    conflict = (
        db.query(SnapshotConflict)
        .filter(SnapshotConflict.snapshot_id == snapshot.id)
        .first()
    )

    if conflict:
        raise HTTPException(409, "Snapshot has unresolved conflict")

def detect_conflict_or_raise(*, db, snapshot, user):
    """
    Phase U-S invariant:
    Conflict detection hook.

    Current behavior:
    - No conflict → allow execution
    - Future: raise on detected conflict

    This function exists to provide a stable kernel guard.
    """
    return None


__all__ = [
    "detect_conflict_or_raise",
]
