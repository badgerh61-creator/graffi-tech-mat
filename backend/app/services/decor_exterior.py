import hashlib
import json
from sqlalchemy.orm import Session

from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services.journal import write_journal_entry


# -------------------------------------------------
# APPLY DECAL
# -------------------------------------------------

def apply_exterior_decal_mutation(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    decal_id: str,
    target: dict,
):
    old_decor = base_snapshot.decor_state or {}
    old_decals = old_decor.get("decals", [])

    new_decor_state = {
        **old_decor,
        "decals": [
            *old_decals,
            {
                "instance_id": decal_id,
                "target": target,
            },
        ],
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

    write_journal_entry(
        db=db,
        project_id=project_id,
        intent_type="decor.exterior.apply-decal",
        target_type="snapshot",
        target_id=snapshot.id,
        before_state={"snapshot_id": base_snapshot.id},
        after_state={"snapshot_id": snapshot.id},
        issued_by_user_id=user_id,
    )

    return snapshot


# -------------------------------------------------
# REMOVE DECAL
# -------------------------------------------------

def remove_exterior_decal_mutation(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    decal_instance_id: str,
):
    old_decor = base_snapshot.decor_state or {}
    old_decals = old_decor.get("decals", [])

    # ✅ REQUIRED BY TEST — missing instance = 404
    if not any(d["instance_id"] == decal_instance_id for d in old_decals):
        raise KeyError("Decal instance not found")

    new_decals = [
        d for d in old_decals if d["instance_id"] != decal_instance_id
    ]

    new_decor_state = {
        **old_decor,
        "decals": new_decals,
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

    write_journal_entry(
        db=db,
        project_id=project_id,
        intent_type="decor.exterior.remove-decal",
        target_type="snapshot",
        target_id=snapshot.id,
        before_state={"snapshot_id": base_snapshot.id},
        after_state={"snapshot_id": snapshot.id},
        issued_by_user_id=user_id,
    )

    return snapshot

