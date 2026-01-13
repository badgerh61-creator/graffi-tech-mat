# backend/app/services/set_engine_tune.py

from fastapi.responses import JSONResponse
import json
import hashlib

from app.services.tuning_presets import get_engine_tune_preset
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.journal_entry import JournalEntry
from app.validation.tuning.errors import (
    InvalidSnapshotBase,
    EngineTunePresetNotFound,
)


def _hash_scene_and_tuning(scene_state, tuning_state):
    """
    Canonical deterministic hash helper (Phase K.2).
    MUST exactly match test behavior.
    """
    payload = {
        "scene": scene_state or {},
        "tuning": tuning_state or {},
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def set_engine_tune(*, db, user, payload: dict):
    """
    Phase K.2 — Engine tune preset (read-only, deterministic)
    Mirrors set_suspension_preset EXACTLY.
    """

    project_id = payload.get("project_id")
    snapshot_base_id = payload.get("snapshot_base_id")
    preset_id = payload.get("preset_id")

    if not project_id or not snapshot_base_id or not preset_id:
        raise ValueError("project_id, snapshot_base_id, and preset_id required")

    # ✅ STEP 1 — snapshot base validation
    snapshot = db.get(RenderedSnapshot, snapshot_base_id)
    if (
        snapshot is None
        or snapshot.project_id != project_id
        or snapshot.status != "completed"
        or snapshot.is_obsolete
    ):
        return JSONResponse(
            status_code=InvalidSnapshotBase.status_code,
            content={"error": InvalidSnapshotBase.error_code},
        )

    # ✅ STEP 2 — preset resolution (READ-ONLY)
    preset = get_engine_tune_preset(preset_id)
    if preset is None:
        return JSONResponse(
            status_code=EngineTunePresetNotFound.status_code,
            content={"error": EngineTunePresetNotFound.error_code},
        )

    # ✅ STEP 3 — capability gate (EXPLICIT, PHASE K.2 SAFE)
    if not getattr(user, "can_tune", False):
        return JSONResponse(
            status_code=403,
            content={"error": "tuning_capability_required"},
        )

    # ✅ STEP 4 — tuning state (Phase K.2 scope)
    tuning_state = {
        "engine": {
            "preset_id": preset_id,
        }
    }

    scene_state_hash = _hash_scene_and_tuning(
        scene_state={},          # Phase K.2 does NOT mutate scene
        tuning_state=tuning_state,
    )

    # ✅ STEP 5 — create OR reuse snapshot (deterministic)
    existing = (
        db.query(RenderedSnapshot)
        .filter_by(
            project_id=snapshot.project_id,
            scene_state_hash=scene_state_hash,
            render_profile=snapshot.render_profile,
            engine_version=snapshot.engine_version,
        )
        .first()
    )

    if existing:
        new_snapshot = existing
    else:
        new_snapshot = RenderedSnapshot(
            project_id=snapshot.project_id,
            scene_state_hash=scene_state_hash,
            render_profile=snapshot.render_profile,
            engine_version=snapshot.engine_version,
            status="completed",
            created_by=user.id,
            tuning_state=tuning_state,
        )
        db.add(new_snapshot)
        db.commit()
        db.refresh(new_snapshot)

    # ✅ STEP 6 — journal entry (schema-complete)
    entry = JournalEntry(
        project_id=project_id,
        mutation_type="tuning.set-engine-tune",  # EXACT string
        snapshot_before=snapshot.id,
        snapshot_after=new_snapshot.id,
        snapshot_id=new_snapshot.id,
        actor_id=user.id,
    )

    db.add(entry)
    db.commit()

    return {
        "status": "ok",
        "snapshot_id": new_snapshot.id,
    }

