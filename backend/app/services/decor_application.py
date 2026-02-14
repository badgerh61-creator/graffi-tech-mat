# backend/app/services/decor_application.py

from fastapi import HTTPException
from app.models.rendered_snapshot import SnapshotStatus
from app.services.audit import log_event


def apply_decor_preset(*, db, snapshot, preset: dict, user):
    """
    Tier 3.5 — Controlled Preset Application (AUTHORITATIVE)

    Rules:
    - Snapshot must be draft
    - User must own draft
    - Creates new draft snapshot (immutable lineage)
    - Preset metadata recorded inside decor_state
    - Emits audit event
    """

    if snapshot.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(409, "Snapshot must be draft")

    if snapshot.owner_user_id != user.id:
        raise HTTPException(403, "Not draft owner")

    # ---------------------------------------------
    # Clone snapshot safely
    # ---------------------------------------------

    new_snapshot = snapshot.clone_for_mutation(created_by=user.id)

    # ---------------------------------------------
    # Apply preset to decor_state
    # ---------------------------------------------

    base_decor = snapshot.decor_state or {}
    updated_decor = dict(base_decor)

    updated_decor.update(preset.get("decor", {}))

    # Store preset metadata under reserved key
    updated_decor["_applied_presets"] = (
        base_decor.get("_applied_presets", [])
        + [
            {
                "preset_id": preset["name"],
                "preset_version": preset["version"],
            }
        ]
    )

    new_snapshot.decor_state = updated_decor

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    # ---------------------------------------------
    # Emit audit event
    # ---------------------------------------------

    log_event(
        db=db,
        user_id=user.id,
        action="snapshot.decor_preset_applied",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        extra={
            "preset_id": preset["name"],
            "preset_version": preset["version"],
        },
    )

    db.commit()

    return new_snapshot


