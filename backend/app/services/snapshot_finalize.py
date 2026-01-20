from datetime import datetime
from app.models.snapshot import Snapshot

def finalize_draft_snapshot(db, *, snapshot, user):
    if snapshot.status != "draft":
        raise HTTPException(409, "Only draft snapshots can be finalized")

    completed = Snapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        status="completed",
        created_by_id=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(completed)
    db.delete(snapshot)
    db.commit()
    db.refresh(completed)

    return completed

