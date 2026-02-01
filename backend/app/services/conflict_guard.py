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

