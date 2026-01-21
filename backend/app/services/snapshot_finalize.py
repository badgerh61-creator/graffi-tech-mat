from datetime import datetime
from fastapi import HTTPException, status

from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services import audit


def finalize_snapshot(*, db, snapshot: RenderedSnapshot, user):
    """
    Phase 4.5 — Draft Finalization (Service Layer)

    - Only DRAFT snapshots can be finalized
    - Draft is closed (FINALIZED)
    - A NEW immutable COMPLETED snapshot is created
    - History is preserved
    """

    if snapshot.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Only draft snapshots can be finalized",
        )

    if not snapshot.parent_snapshot_id:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Draft snapshot has no parent",
        )

    # 1️⃣ Close draft
    snapshot.status = SnapshotStatus.FINALIZED.value
    snapshot.closed_at = datetime.utcnow()

    # 2️⃣ Create completed snapshot
    completed = RenderedSnapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        status=SnapshotStatus.COMPLETED.value,
        created_by=user.id,
    )

    db.add(completed)
    db.commit()
    db.refresh(completed)

    # 3️⃣ Audit
    audit.log_event(
        db=db,
        user_id=user.id,
        action="snapshot.finalized",
        resource_type="snapshot",
        resource_id=completed.id,
        extra={"source_draft_id": snapshot.id},
    )

    return completed

