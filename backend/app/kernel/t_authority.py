from fastapi import HTTPException

from app.services.presence_sessions import require_active_session
from app.services.draft_lock_service import acquire_draft_lock, get_draft_lock
from app.services.audit import log_event


def require_draft_authority(*, db, user, snapshot):
    # Phase U.1 — session authority
    try:
        require_active_session(
            db=db,
            user=user,
            project_id=snapshot.project_id,
            snapshot_id=snapshot.id,
        )
    except HTTPException:
        log_event(
            db=db,
            user_id=user.id,
            action="authority.violation",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "session_expired"},
        )
        raise

    # Phase T — lifecycle enforcement
    if snapshot.status != "draft":
        log_event(
            db=db,
            user_id=user.id,
            action="authority.violation",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "snapshot_not_draft"},
        )
        raise HTTPException(409, "Snapshot not draft")

    # Phase U.2 — draft ownership (LOCK-AWARE)
    lock = get_draft_lock(db=db, snapshot=snapshot)

    if lock is None:
        acquire_draft_lock(db=db, snapshot=snapshot, user=user)
        return

    if lock.user_id != user.id:
        log_event(
            db=db,
            user_id=user.id,
            action="authority.violation",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "not_draft_owner"},
        )
        raise HTTPException(403, "Not draft owner")

