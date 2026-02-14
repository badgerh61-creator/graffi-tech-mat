# backend/app/services/snapshot_access.py

from fastapi import HTTPException
from app.services import audit


def require_snapshot_owner(*, db, snapshot, user):
    """
    Phase U invariant:
    - Draft ownership is authoritative
    - Non-owners may NEVER mutate
    - Violation MUST audit + raise
    """

    if snapshot.owner_user_id is None:
        audit.log_event(
            db=db,
            user_id=user.id,
            action="snapshot.access_denied",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "no_owner"},
        )
        db.flush()
        raise HTTPException(403, "Draft has no owner")

    if snapshot.owner_user_id != user.id:
        audit.log_event(
            db=db,
            user_id=user.id,
            action="snapshot.access_denied",
            resource_type="snapshot",
            resource_id=snapshot.id,
            extra={"reason": "not_owner"},
        )
        db.flush()
        raise HTTPException(403, "Not draft owner")

    return snapshot

