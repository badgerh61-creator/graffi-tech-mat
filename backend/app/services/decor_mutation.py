# backend/app/services/decor_mutation.py

from datetime import datetime
from fastapi import HTTPException

from app.models.snapshot import Snapshot
from app.services.audit import log_event


ALLOWED_DECOR_OPERATIONS = {
    "decor.apply_material",
    "decor.replace_preset",
    "decor.remove",
}


def apply_decor_change(
    *,
    db,
    snapshot,
    user,
    operation: str,
    target_id: str | None = None,
    params: dict | None = None,
):
    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not editable")

    if operation not in ALLOWED_DECOR_OPERATIONS:
        raise HTTPException(422, "Invalid decor operation")

    new_snapshot = Snapshot(
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
    db.commit()
    db.refresh(new_snapshot)

    # ✅ FIXED ACTION STRING
    log_event(
        db=db,
        user_id=user.id,
        action="snapshot.decor.edit",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
    )

    return new_snapshot

