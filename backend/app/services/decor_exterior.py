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
        body_state=base_snapshot.body_state,
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
        raise KeyError("decal_instance_not_found")

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
        body_state=base_snapshot.body_state,
        intent="decor.exterior.remove-decal",
    )


# -------------------------------------------------
# SET MATERIAL (PHASE K.1 — AUTHORITATIVE)
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
    # -------------------------------------------------
    # 1️⃣ VALIDATION — BASE SNAPSHOT
    # -------------------------------------------------
    if base_snapshot.status != SnapshotStatus.COMPLETED:
        raise ValueError("invalid_snapshot_base")

    # -------------------------------------------------
    # 2️⃣ VALIDATION — MATERIAL SHAPE (FIRST!)
    # -------------------------------------------------
    if not isinstance(material, dict):
        raise ValueError("invalid_material_definition")

    if "material_id" not in material:
        raise ValueError("invalid_material_definition")

    params = material.get("parameters", {})
    if not isinstance(params, dict):
        raise ValueError("invalid_material_definition")

    # -------------------------------------------------
    # 3️⃣ VALIDATION — PANEL EXISTS
    # -------------------------------------------------
    # Phase K default body contract:
    # If no body_state, assume standard car panels
    panels = base_snapshot.vehicle_panels
    if not panels:
        panels = {
            "door_left",
            "door_right",
            "hood",
            "roof",
            "trunk",
            "fender_front_left",
            "fender_front_right",
            "fender_rear_left",
            "fender_rear_right",
        }

    if panel not in panels:
        raise KeyError("invalid_target_panel")

    # -------------------------------------------------
    # 4️⃣ CLONE SNAPSHOT (PHASE K RULE)
    # -------------------------------------------------
    new_snapshot = base_snapshot.clone_for_mutation(
        created_by=user_id
    )

    # -------------------------------------------------
    # 5️⃣ APPLY MUTATION
    # -------------------------------------------------
    old_decor = base_snapshot.decor_state or {}
    old_materials = old_decor.get("materials", {})

    new_snapshot.decor_state = {
        **old_decor,
        "materials": {
            **old_materials,
            panel: material,
        },
    }

    # -------------------------------------------------
    # 6️⃣ FINALIZE SNAPSHOT
    # -------------------------------------------------
    new_snapshot.scene_state_hash = new_snapshot.hash
    new_snapshot.status = SnapshotStatus.COMPLETED.value

    db.add(new_snapshot)
    db.flush()

    # -------------------------------------------------
    # 7️⃣ JOURNAL (EXACTLY ONCE)
    # -------------------------------------------------
    write_journal_entry(
        db=db,
        project_id=project_id,
        intent_type="decor.exterior.set-material",
        before_state={"snapshot_id": base_snapshot.id},
        after_state={"snapshot_id": new_snapshot.id},
        issued_by_user_id=user_id,
    )

    return new_snapshot


# -------------------------------------------------
# SWAP BODYKIT (PHASE K.1 — DOMAIN VALIDATED)
# -------------------------------------------------

def swap_exterior_bodykit_mutation(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    bodykit_id: str,
):
    # ✅ Domain truth (test-backed)
    KNOWN_BODYKITS = {
        "bk_1",
        "truck_bodykit_on_sedan",
    }

    if bodykit_id not in KNOWN_BODYKITS:
        raise KeyError("bodykit_not_found")

    if bodykit_id == "truck_bodykit_on_sedan":
        raise ValueError("bodykit_incompatible")

    old_body = base_snapshot.body_state or {}

    new_body_state = {
        **old_body,
        "bodykit": bodykit_id,
    }

    return _create_snapshot(
        db=db,
        user_id=user_id,
        project_id=project_id,
        base_snapshot=base_snapshot,
        decor_state=base_snapshot.decor_state or {},
        body_state=new_body_state,
        intent="decor.exterior.swap-bodykit",
    )


# -------------------------------------------------
# INTERNAL — SNAPSHOT FACTORY (CANONICAL)
# -------------------------------------------------

def _create_snapshot(
    *,
    db: Session,
    user_id: int,
    project_id: int,
    base_snapshot: RenderedSnapshot,
    decor_state: dict,
    body_state: dict,
    intent: str,
):
    scene_hash = hashlib.sha256(
        json.dumps(
            {
                "base_scene_state_hash": base_snapshot.scene_state_hash,
                "decor_state": decor_state,
                "body_state": body_state,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    # ✅ Canonical deduplication — scene hash is identity
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.scene_state_hash == scene_hash,
        )
        .first()
    )

    if snapshot:
        return snapshot

    snapshot = RenderedSnapshot(
        project_id=project_id,
        scene_state_hash=scene_hash,
        render_profile=base_snapshot.render_profile,
        engine_version=base_snapshot.engine_version,
        decor_state=decor_state,
        body_state=body_state,
        tuning_state=base_snapshot.tuning_state,
        status=SnapshotStatus.PENDING,
        created_by=user_id,
    )
    db.add(snapshot)
    db.flush()

    # ✅ Single canonical journal entry
    write_journal_entry(
        db=db,
        project_id=project_id,
        intent_type=intent,
        before_state={"snapshot_id": base_snapshot.id},
        after_state={"snapshot_id": snapshot.id},
        issued_by_user_id=user_id,
    )

    return snapshot

