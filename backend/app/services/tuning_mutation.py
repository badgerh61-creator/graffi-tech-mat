# backend/app/services/tuning_mutation.py

"""
Tier 4.3 — Controlled Tuning Mutation

Compatible with:
- Direct service call (legacy phases)
- ToolExecutor governed call (Tier 4.3+)
"""

from fastapi import HTTPException

from app.services.snapshot_cloner import clone_snapshot
from app.services.tuning_state import apply_suspension_preset
from app.services.tuning_presets import (
    get_suspension_preset,
    get_engine_tune_preset,
)
from app.services.audit import log_event

# -------------------------------------------------------
# ENGINE CONFIG UPDATE
# -------------------------------------------------------

def update_engine_config(*, db, snapshot, user, payload=None, params=None):

    data = payload or params
    if not data:
        raise HTTPException(422, "Missing payload")

    if not getattr(snapshot, "_validated_by_executor", False):
        from app.services.draft_lock_service import require_draft_owner
        require_draft_owner(db=db, snapshot=snapshot, user=user)

    preset_id = data.get("preset_id")
    if not preset_id:
        raise HTTPException(422, "Missing preset_id")

    preset = get_engine_tune_preset(preset_id)
    if not preset:
        raise HTTPException(422, f"Unknown engine preset: {preset_id}")

    new_snapshot = clone_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    tuning_state = dict(new_snapshot.tuning_state or {})
    tuning_state["engine"] = preset
    new_snapshot.tuning_state = tuning_state

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    # ✅ DOMAIN AUDIT EVENT
    log_event(
        db=db,
        user_id=user.id,
        action="snapshot.tuning_updated",
        resource_type="snapshot",
        resource_id=new_snapshot.id,
        extra={
            "parent_snapshot_id": snapshot.id,
            "preset_id": preset_id,
            "component": "engine",
        },
    )

    return new_snapshot


# -------------------------------------------------------
# SUSPENSION CONFIG UPDATE
# -------------------------------------------------------

def update_suspension_config(*, db, snapshot, user, payload=None, params=None):

    data = payload or params
    if not data:
        raise HTTPException(422, "Missing payload")

    if not getattr(snapshot, "_validated_by_executor", False):
        from app.services.draft_lock_service import require_draft_owner
        require_draft_owner(db=db, snapshot=snapshot, user=user)

    preset_id = data.get("preset_id")
    if not preset_id:
        raise HTTPException(422, "Missing preset_id")

    preset = get_suspension_preset(preset_id)
    if not preset:
        raise HTTPException(422, f"Unknown suspension preset: {preset_id}")

    new_snapshot = clone_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    base_state = dict(new_snapshot.tuning_state or {})

    next_state = apply_suspension_preset(
        base_state=base_state,
        preset=preset,
    )

    new_snapshot.tuning_state = next_state

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    return new_snapshot

