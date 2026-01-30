from fastapi import HTTPException
from app.services.draft_lock_service import get_draft_lock, acquire_draft_lock, release_draft_lock
from app.services.presence_service import is_user_present
from app.services.conflict_detector import detect_conflict
from app.services.audit import log_event

def handoff_draft_ownership(*, db, snapshot, from_user, to_user):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    lock = get_draft_lock(db=db, snapshot=snapshot)
    if not lock or lock.user_id != from_user.id:
        raise HTTPException(403, "Not draft owner")

    if not is_user_present(db=db, user=to_user):
        raise HTTPException(409, "Target user not present")

    if detect_conflict(db=db, snapshot=snapshot, user=from_user):
        raise HTTPException(409, "Draft has unresolved conflict")

    # 🔁 atomic swap
    release_draft_lock(db=db, snapshot=snapshot, user=from_user)
    new_lock = acquire_draft_lock(db=db, snapshot=snapshot, user=to_user)

    log_event(
        db,
        action="draft.handoff.completed",
        resource_id=snapshot.id,
        user_id=from_user.id,
        extra={"to_user_id": to_user.id},
    )

    return new_lock

