from fastapi import HTTPException
from datetime import datetime

def apply_decor_change(*, db, snapshot, user, operation, target_id, params):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not editable")

    if not user.has_capability("canEditExteriorDecor"):
        raise HTTPException(403, "Capability missing")

    new_snapshot = snapshot.clone_as_draft(
        created_by=user.id,
        created_at=datetime.utcnow(),
    )

    new_snapshot.commands.append({
        "type": operation,
        "target": target_id,
        "params": params,
    })

    db.add(new_snapshot)
    db.commit()

    return new_snapshot

