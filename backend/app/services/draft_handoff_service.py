# backend/app/services/draft_handoff_service.py

from fastapi import HTTPException

from app.models.draft_lock import DraftLock
from app.models.conflict import SnapshotConflict
from app.services.presence_service import is_user_present
from app.services.audit import log_event


def handoff_draft_ownership(*, db, snapshot, from_user, to_user):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    # 🔒 Phase U.4 — EXPLICIT conflicts block handoff
    explicit = (
        db.query(SnapshotConflict)
        .filter(SnapshotConflict.snapshot_id == snapshot.id)
        .first()
    )
    if explicit:
        raise HTTPException(409, "Draft is conflicted")

    lock = (
        db.query(DraftLock)
        .filter_by(snapshot_id=snapshot.id)
        .first()
    )
    if not lock:
        raise HTTPException(409, "Draft not locked")

    if lock.user_id != from_user.id:
        raise HTTPException(403, "Not draft owner")

    if not is_user_present(to_user):
        raise HTTPException(409, "Target user not present")

    previous_owner_id = lock.user_id

    lock.user_id = to_user.id
    snapshot.owner_user_id = to_user.id

    db.commit()

    log_event(
        db=db,
        user_id=from_user.id,
        action="draft.handoff",
        resource_type="snapshot",
        resource_id=snapshot.id,
        extra={
            "previous_owner_id": previous_owner_id,
            "new_owner_id": to_user.id,
            "project_id": snapshot.project_id,
        },
    )

    return lock

