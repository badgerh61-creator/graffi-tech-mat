# backend/app/services/draft_handoff_service.py

from fastapi import HTTPException

from app.models.draft_lock import DraftLock
from app.services.presence_service import is_user_present
from app.services.audit import log_event


def handoff_draft_ownership(*, db, snapshot, from_user, to_user):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    lock = (
        db.query(DraftLock)
        .filter_by(snapshot_id=snapshot.id)
        .first()
    )

    if not lock:
        raise HTTPException(409, "Draft not locked")

    # 1️⃣ Authority check FIRST
    if lock.user_id != from_user.id:
        raise HTTPException(403, "Not draft owner")

    # 2️⃣ Presence check (USER ONLY — canonical)
    if not is_user_present(to_user):
        raise HTTPException(409, "Target user not present")

    previous_owner_id = lock.user_id

    # Transfer ownership
    lock.user_id = to_user.id
    snapshot.owner_user_id = to_user.id

    db.commit()

    # Audit
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

