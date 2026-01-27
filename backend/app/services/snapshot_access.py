# backend/app/services/snapshot_access.py
# Phase U — access guard (AUTHORITATIVE)

from fastapi import HTTPException
from app.services import audit
from app.db.session import SessionLocal

def require_snapshot_owner(*, db, snapshot, user):
    
    if snapshot.owner_user_id is None:
        return

    if snapshot.owner_user_id != user.id:
        print(">>> ACCESS DENIED PATH HIT")
        audit.log_event(
            db=db,
            user_id=user.id,
            action="snapshot.access_denied",
            resource_type="snapshot",
            resource_id=snapshot.id,
        )
        db.flush()
        raise HTTPException(status_code=403)

