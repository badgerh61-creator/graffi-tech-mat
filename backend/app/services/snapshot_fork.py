from datetime import datetime
from fastapi import HTTPException

from app.models.rendered_snapshot import RenderedSnapshot
from app.services.audit import log_event


def fork_snapshot(
    *,
    db,
    parent_snapshot,
    user,
    reason: str,
):
    """
    Fork a new draft snapshot from an existing DRAFT snapshot.

    Canonical mutation primitive.
    Used by:
    - Phase 5 transforms
    - Phase U conflict resolution
    - Undo / redo
    - Rebase
    """

    # =====================================================
    # Phase U — lifecycle enforcement
    # =====================================================
    if parent_snapshot.status != "draft":
        raise HTTPException(
            status_code=409,
            detail="Only draft snapshots may be forked",
        )

    # =====================================================
    # Phase U — deterministic fork
    # =====================================================
    new_snapshot = RenderedSnapshot(
        project_id=parent_snapshot.project_id,
        parent_snapshot_id=parent_snapshot.id,
        scene_state_hash=parent_snapshot.scene_state_hash,
        render_profile=parent_snapshot.render_profile,   # ✅ FIX
        engine_version=parent_snapshot.engine_version,
        deterministic_key=parent_snapshot.deterministic_key,
        status="draft",
        created_by=user.id,
        owner_user_id=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    # =====================================================
    # Phase U — audit is authoritative
    # =====================================================
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

