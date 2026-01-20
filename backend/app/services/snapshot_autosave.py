from fastapi import HTTPException
from datetime import datetime

def autosave_draft_snapshot(db, *, snapshot, scene_state_hash):
    if snapshot.status != "draft":
        raise HTTPException(409, "Only draft snapshots can be autosaved")

    snapshot.scene_state_hash = scene_state_hash
    snapshot.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(snapshot)

    return snapshot

