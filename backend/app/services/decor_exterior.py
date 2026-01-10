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
            {"instance_id": decal_id, "target": target},
        ],
    }

    return _create_snapshot(
        db=db,
        user_id=user_id,
        project_id=project_id,
        base_snapshot=base_snapshot,
        decor_state=new_decor_state,
        intent="decor.exterior.apply-decal",
    )


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

    if not any(d["instance_id"] == decal_instance_id for d in old_decals):
        raise KeyError("Decal instance not found")

    new_decor_state = {
        **old_decor,
        "decals": [
            d for d in old_decals if d["instance_id"] != decal_instance_id
        ],
    }

    return _create_snapshot(
        db=db,
        user_id=user_id,
        project_id=project_id,
        base_snapshot=base_snapshot,
        decor_state=new_decor_state,
        intent="decor.exterior.remove-decal",
    )


# -------------------------------------------------
# SET MATERIAL
# -------------------------------------------------

def set_exterior_material_mutation(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    panel: str,
    material: dict,
):
    old_decor = base_snapshot.decor_state or {}
    old_materials = old_decor.get("materials", {})

    new_decor_state = {
        **old_decor,
        "materials": {
            **old_materials,
            panel: material,
        },
    }

    return _create_snapshot(
        db=db,
        user_id=user_id,
        project_id=project_id,
        base_snapshot=base_snapshot,
        decor_state=new_decor_state,
        intent="decor.exterior.set-material",
    )


# -------------------------------------------------
# INTERNAL — SNAPSHOT FACTORY (FINAL, CORRECT)
# -------------------------------------------------

def _create_snapshot(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    decor_state: dict,
    intent: str,
):
    scene_hash = hashlib.sha256(
        json.dumps(
            {
                "base_scene_state_hash": base_snapshot.scene_state_hash,
                "decor_state": decor_state,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.scene_state_hash == scene_hash,
            RenderedSnapshot.render_profile == base_snapshot.render_profile,
            RenderedSnapshot.engine_version == base_snapshot.engine_version,
        )
        .first()
    )

    if not snapshot:
        snapshot = RenderedSnapshot(
            project_id=project_id,
            scene_state_hash=scene_hash,
            render_profile=base_snapshot.render_profile,
            engine_version=base_snapshot.engine_version,
            decor_state=decor_state,
            tuning_state=base_snapshot.tuning_state,
            body_state=base_snapshot.body_state,
            status=SnapshotStatus.PENDING,
            created_by=user_id,
        )
        db.add(snapshot)
        db.flush()

        # ✅ Phase K canonical journaling (correct signature)
        write_journal_entry(
            db=db,
            project_id=project_id,
            intent_type=intent,
            before_state={"snapshot_id": base_snapshot.id},
            after_state={"snapshot_id": snapshot.id},
            issued_by_user_id=user_id,
        )

    return snapshot

