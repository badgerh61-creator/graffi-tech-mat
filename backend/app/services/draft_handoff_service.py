# backend/app/services/draft_handoff_service.py

from fastapi import HTTPException

from app.models.rendered_snapshot import RenderedSnapshot
from app.models.conflict import SnapshotConflict
from app.services.presence_service import is_user_present
from app.services.audit import log_event


from datetime import datetime

def handoff_draft_ownership(*, db, snapshot, from_user, to_user):

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot.id)
        .with_for_update()
        .one()
    )

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    if db.query(SnapshotConflict).filter(
        SnapshotConflict.snapshot_id == snapshot.id
    ).first():
        raise HTTPException(409, "Draft is conflicted")

    if from_user.role == "viewer":
        raise HTTPException(403, "Not draft owner")

    if not is_user_present(to_user):
        raise HTTPException(409, "Target user not present")

    # 🔒 Authority resolution
    if snapshot.owner_user_id is not None and snapshot.owner_user_id != from_user.id:
        if snapshot.locked_at is None:
            raise HTTPException(403, "Not draft owner")

    previous_owner_id = snapshot.owner_user_id

    # 🔁 Atomic transfer
    snapshot.owner_user_id = to_user.id
    snapshot.locked_at = datetime.utcnow()

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

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

    return snapshot

