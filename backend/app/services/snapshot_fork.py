# Phase U — fork service (stub)

from datetime import datetime
from fastapi import HTTPException

from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services import audit


def fork_snapshot(*, db, snapshot, user):
    if snapshot.status not in (
        SnapshotStatus.COMPLETED.value,
        SnapshotStatus.FINALIZED.value,
    ):
        raise HTTPException(
            status_code=409,
            detail="Only completed snapshots may be forked",
        )

    fork = RenderedSnapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        status=SnapshotStatus.DRAFT.value,
        parent_snapshot_id=snapshot.id,
        created_by=user.id,
        owner_user_id=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(fork)
    db.commit()
    db.refresh(fork)

    audit.log_event(
        db=db,
        user_id=user.id,
        action="snapshot.forked",
        resource_type="snapshot",
        resource_id=fork.id,
        extra={"parent_snapshot_id": snapshot.id},
    )

    return fork

