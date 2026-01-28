from fastapi import HTTPException
from app.services.draft_lock_service import get_draft_lock

def require_draft_ownership(*, db, snapshot, user):
    lock = get_draft_lock(db=db, snapshot=snapshot)

    if not lock or lock.user_id != user.id:
        raise HTTPException(403, "Draft not owned by user")

