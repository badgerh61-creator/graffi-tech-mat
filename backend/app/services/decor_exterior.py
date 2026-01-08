import hashlib
import json
from sqlalchemy.orm import Session

from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services.journal import write_journal_entry


def apply_exterior_decal_mutation(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    decal_id: str,
    target: dict,
):
    # ---------------------------------------------------------
    # Deterministic state transform (PURE)
    # ---------------------------------------------------------
    new_decor_state = {
        **(base_snapshot.decor_state or {}),
        "applied_decal": {
            "decal_id": decal_id,
            "target": target,
        },
    }

    new_scene_state_hash = hashlib.sha256(
        json.dumps(
            {
                "base_scene_state_hash": base_snapshot.scene_state_hash,
                "decor_state": new_decor_state,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    # ---------------------------------------------------------
    # Deterministic deduplication (Phase I / J)
    # ---------------------------------------------------------
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.scene_state_hash == new_scene_state_hash,
            RenderedSnapshot.render_profile == base_snapshot.render_profile,
            RenderedSnapshot.engine_version == base_snapshot.engine_version,
        )
        .first()
    )

    if not snapshot:
        snapshot = RenderedSnapshot(
            project_id=project_id,
            scene_state_hash=new_scene_state_hash,
            render_profile=base_snapshot.render_profile,
            engine_version=base_snapshot.engine_version,
            decor_state=new_decor_state,
            tuning_state=base_snapshot.tuning_state,
            body_state=base_snapshot.body_state,
            status=SnapshotStatus.PENDING,
            created_by=user_id,
        )
        db.add(snapshot)
        db.flush()

    # ---------------------------------------------------------
    # Journaling (MANDATORY)
    # ---------------------------------------------------------
    write_journal_entry(
        db=db,
        intent_type="decor.exterior.apply-decal",
        target_type="snapshot",
        target_id=snapshot.id,
        before_state={
            "snapshot_id": base_snapshot.id,
            "decor_state": base_snapshot.decor_state,
        },
        after_state={
            "snapshot_id": snapshot.id,
            "decor_state": new_decor_state,
        },
        issued_by_user_id=user_id,
    )

    return snapshot

