# app/api/mutations/body/apply_morph.py

import hashlib
import json

from app.schemas.body import BodyMorphApplyPayload
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.journal_entry import JournalEntry

from app.services.capabilities import require_capability
from app.services.rendering import render_snapshot
from app.services.body_state import apply_body_morph as apply_body_state
from app.services.body_presets import get_body_morph_preset

from app.validation.body.rules import (
    validate_base_snapshot,
    validate_body_preset,
    validate_body_parameters,
)
from app.validation.body.errors import (
    BodyPresetNotFound,
    BodyParametersOutOfBounds,
)


def apply_body_morph(*, db, user, payload: BodyMorphApplyPayload):
    # -------------------------------------------------
    # STEP 0 — Capability gate (REQUIRED)
    # -------------------------------------------------
    require_capability(
        db=db,
        user=user,
        project_id=payload.project_id,
        capability="body_edit",
    )

    # -------------------------------------------------
    # STEP 1 — Snapshot base validation
    # -------------------------------------------------
    base_snapshot = db.get(RenderedSnapshot, payload.base_snapshot_id)
    validate_base_snapshot(base_snapshot)

    # -------------------------------------------------
    # STEP 2 — Preset resolution
    # -------------------------------------------------
    preset = get_body_morph_preset(payload.preset_id)
    if preset is None:
        raise BodyPresetNotFound()

    validate_body_preset(
        preset,
        snapshot=base_snapshot,
    )

    # -------------------------------------------------
    # STEP 3 — Parameter validation (MUST be before hashing)
    # -------------------------------------------------
    validate_body_parameters(preset, payload.parameters)

    # -------------------------------------------------
    # STEP 4 — PURE body morph application
    # -------------------------------------------------
    new_body_state = apply_body_state(
        base_state=base_snapshot.body_state,
        preset=preset,
        parameters=payload.parameters,
    )

    # -------------------------------------------------
    # STEP 5 — Canonical scene state + deterministic hash
    # -------------------------------------------------
    scene_state = {
        "decor": base_snapshot.decor_state,
        "tuning": base_snapshot.tuning_state,
        "body": new_body_state,
    }

    canonical = json.dumps(
        scene_state,
        sort_keys=True,
        separators=(",", ":"),
    )
    scene_state_hash = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()

    # -------------------------------------------------
    # STEP 6 — Deduplicate identical snapshot
    # -------------------------------------------------
    existing = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == base_snapshot.project_id,
            RenderedSnapshot.scene_state_hash == scene_state_hash,
            RenderedSnapshot.render_profile == base_snapshot.render_profile,
            RenderedSnapshot.engine_version == base_snapshot.engine_version,
            RenderedSnapshot.status == SnapshotStatus.COMPLETED,
        )
        .first()
    )

    if existing:
        return {
            "snapshot_id": existing.id,
            "hash": existing.hash,
        }

    # -------------------------------------------------
    # STEP 7 — Render
    # -------------------------------------------------
    image_url = render_snapshot(
        scene_state=scene_state,
        render_profile=base_snapshot.render_profile,
    )

    # -------------------------------------------------
    # STEP 8 — Immutable snapshot creation
    # -------------------------------------------------
    new_snapshot = RenderedSnapshot(
        project_id=base_snapshot.project_id,
        scene_state_hash=scene_state_hash,
        render_profile=base_snapshot.render_profile,
        engine_version=base_snapshot.engine_version,
        decor_state=scene_state["decor"],
        tuning_state=scene_state["tuning"],
        body_state=scene_state["body"],
        image_url=image_url,
        status=SnapshotStatus.COMPLETED,
        created_by=user.id,
    )

    db.add(new_snapshot)
    db.commit()
    db.refresh(new_snapshot)

    # -------------------------------------------------
    # STEP 9 — Journal entry (REQUIRED)
    # -------------------------------------------------
    journal = JournalEntry(
        project_id=base_snapshot.project_id,
        mutation_type="body.apply_morph",
        snapshot_before=base_snapshot.id,
        snapshot_after=new_snapshot.id,
        actor_id=user.id,
    )

    db.add(journal)
    db.commit()

    return {
        "snapshot_id": new_snapshot.id,
        "hash": new_snapshot.hash,
    }

