from fastapi import HTTPException
from app.services.presence_sessions import require_active_session
from app.services.draft_lock_service import get_draft_lock
from app.services.audit import log_event


def require_draft_authority(*, db, user, snapshot):

    # 1️⃣ Draft lifecycle
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    # 2️⃣ Lock enforcement FIRST (so audit fires)
    lock = get_draft_lock(db=db, snapshot=snapshot)

    if lock is None or lock.user_id != user.id:
        log_event(
            db=db,
            user_id=user.id,
            action="authority.violation",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "not_draft_owner"},
        )
        db.flush()
        raise HTTPException(403, "Not draft owner")

    # 3️⃣ Session check AFTER ownership
    require_active_session(
        db=db,
        user=user,
        project_id=snapshot.project_id,
        snapshot_id=snapshot.id,
    )

