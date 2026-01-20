from datetime import datetime
from fastapi import HTTPException

from app.models.snapshot import Snapshot


def create_draft_snapshot(db, *, snapshot, user):
    if snapshot.status != "completed":
        raise HTTPException(409, "Only completed snapshots can be drafted")

    existing = (
        db.query(Snapshot)
        .filter(
            Snapshot.project_id == snapshot.project_id,
            Snapshot.status == "draft",
        )
        .first()
    )

    if existing:
        raise HTTPException(409, "Draft snapshot already exists")

    draft = Snapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        status="draft",
        parent_snapshot_id=snapshot.id,
        created_by_id=user.id,
        created_at=datetime.utcnow(),
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)

    return draft

