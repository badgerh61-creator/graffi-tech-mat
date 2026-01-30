from datetime import datetime
from fastapi import HTTPException

from app.models.snapshot import Snapshot
from app.services.audit import log_event


def fork_snapshot(
    *,
    db,
    parent_snapshot,
    user,
    reason: str,
):
    """
    Fork a new draft snapshot from an existing snapshot.

    Canonical mutation primitive.
    Used by:
    - Phase 5 transforms
    - Phase U conflict resolution
    - Undo / redo
    - Rebase
    """

    if parent_snapshot.status != "draft":
        raise HTTPException(
            status_code=409,
            detail="Only draft snapshots may be forked",
        )

    new_snapshot = Snapshot(
        project_id=parent_snapshot.project_id,
        parent_snapshot_id=parent_snapshot.id,
        scene_state_hash=parent_snapshot.scene_state_hash,
        engine_version=parent_snapshot.engine_version,
        status="draft",
        created_by=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    log_event(
        db,
        action="snapshot.forked",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        user_id=user.id,
        extra={
            "parent_snapshot_id": parent_snapshot.id,
            "reason": reason,
        },
    )

    return new_snapshot

