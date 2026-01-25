from datetime import datetime
from fastapi import HTTPException

from app.models.rendered_snapshot import RenderedSnapshot


def clone_snapshot(*, db, snapshot, user):
    """
    Immutable snapshot cloning primitive.

    - NEVER mutates the original snapshot
    - ALWAYS creates a new draft snapshot
    - ALWAYS sets parent_snapshot_id
    """

    if snapshot.status != "draft":
        raise HTTPException(
            status_code=409,
            detail="Only draft snapshots can be cloned",
        )

    new_snapshot = RenderedSnapshot(
        project_id=snapshot.project_id,
        parent_snapshot_id=snapshot.id,
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        status="draft",
        created_by=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(new_snapshot)
    db.flush()  # ensure ID is available immediately

    return new_snapshot

