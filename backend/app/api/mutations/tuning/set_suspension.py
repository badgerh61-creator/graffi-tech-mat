# backend/app/api/mutations/tuning/set_suspension.py

from fastapi.responses import JSONResponse
import json
import hashlib

from app.services.capabilities import require_capability
from app.services.tuning_presets import get_suspension_preset
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.journal_entry import JournalEntry
from app.validation.tuning.errors import (
    InvalidSnapshotBase,
    SuspensionPresetNotFound,
)


def _hash_scene_and_tuning(scene_state, tuning_state):
    """
    Canonical deterministic hash helper (Phase K.2).
    Must exactly match test behavior.
    """
    payload = {
        "scene": scene_state or {},
        "tuning": tuning_state or {},
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def set_suspension_preset(*, db, user, payload):
    """
    Phase K.2
    STEP 1 — Snapshot base validation
    STEP 2 — Preset resolution
    STEP 3 — Capability gate
    STEP 4 — Journal entry
    STEP 5 — Deterministic snapshot creation
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
    preset = get_suspension_preset(preset_id)
    if preset is None:
        return JSONResponse(
            status_code=SuspensionPresetNotFound.status_code,
            content={"error": SuspensionPresetNotFound.error_code},
        )

    # ✅ STEP 3 — capability gate
    require_capability(
        db=db,
        user=user,
        project_id=project_id,
        capability="canTune",
    )

    # ✅ STEP 4 — tuning state (Phase K.2 scope)
    tuning_state = {
        "suspension": {
            "preset_id": preset_id,
        }
    }

    scene_state_hash = _hash_scene_and_tuning(
        scene_state={},        # Phase K.2 does NOT mutate scene
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
        mutation_type="tuning.set-suspension",  # EXACT string
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

