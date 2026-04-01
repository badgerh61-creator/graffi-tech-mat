# backend/app/api/snapshots.py

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user, require_editor
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.schemas import SnapshotCreate, SnapshotRead
from app.services.rendering import render_snapshot
from app.core.config import settings

from app.services.snapshot_finalize import finalize_snapshot
from app.services.scene_index_service import build_scene_index

from sqlalchemy.orm.attributes import flag_modified

from app.models.asset import Asset
from app.models.model import ModelRecord
from app import crud


# -------------------------------------------------
# Project-scoped snapshot routes (Phase 3 → Phase 4)
# -------------------------------------------------

router = APIRouter(
    prefix="/projects/{project_id}/snapshots",
    tags=["Snapshots"],
)

# =================================================
# Phase 3 — Read-only snapshot listing
# =================================================

@router.get("/", response_model=list[SnapshotRead])
def list_snapshots(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase 3
    - Returns ALL snapshots for project
    - Frontend decides which is active
    """
    return (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )


# =================================================
# Phase 3 — Create completed snapshot (rendered)
# =================================================

@router.post("/", response_model=SnapshotRead)
def create_snapshot(
    project_id: int,
    snapshot_in: SnapshotCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    existing = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.scene_state_hash == snapshot_in.scene_state_hash,
            RenderedSnapshot.render_profile == snapshot_in.render_profile,
            RenderedSnapshot.engine_version == settings.ENGINE_VERSION,
            RenderedSnapshot.status == SnapshotStatus.COMPLETED.value,
        )
        .first()
    )

    if existing:
        return existing

    snapshot = RenderedSnapshot(
        project_id=project_id,
        scene_state_hash=snapshot_in.scene_state_hash,
        render_profile=snapshot_in.render_profile,
        engine_version=settings.ENGINE_VERSION,
        status=SnapshotStatus.RUNNING.value,
        created_by=user.id,
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    try:
        image_url = render_snapshot({}, snapshot.render_profile)
        snapshot.image_url = image_url
        snapshot.status = SnapshotStatus.COMPLETED.value
        snapshot.deterministic_key = (
            f"{snapshot.project_id}:"
            f"{snapshot.scene_state_hash}:"
            f"{snapshot.render_profile}:"
            f"{snapshot.engine_version}"
        )
    except Exception as e:
        snapshot.status = SnapshotStatus.FAILED.value
        snapshot.error_message = str(e)

    db.commit()
    db.refresh(snapshot)
    return snapshot


# =================================================
# Phase 4.1 — Create draft snapshot
# =================================================

@router.post("/{snapshot_id}/draft")
def create_draft_snapshot(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.status != SnapshotStatus.COMPLETED.value:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Only completed snapshots can be drafted",
        )

    existing_draft = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.status == SnapshotStatus.DRAFT.value,
        )
        .first()
    )

    if existing_draft:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Draft snapshot already exists for this project",
        )

    draft = RenderedSnapshot(
        project_id=snapshot.project_id,
        scene_state_hash=snapshot.scene_state_hash,
        render_profile=snapshot.render_profile,
        engine_version=snapshot.engine_version,
        status=SnapshotStatus.DRAFT.value,
        parent_snapshot_id=snapshot.id,
        created_by=user.id,
    )

    db.add(draft)
    db.commit()
    db.refresh(draft)

    return {
        "id": draft.id,
        "status": draft.status,
        "parent_snapshot_id": snapshot.id,
    }


# =================================================
# Phase 4.3 — Draft autosave (overwrite same draft)
# =================================================

@router.patch("/{snapshot_id}/autosave")
def autosave_draft_snapshot(
    project_id: int,
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Only draft snapshots can be autosaved",
        )

    if "scene_state_hash" not in payload:
        raise HTTPException(400, "scene_state_hash is required")

    snapshot.scene_state_hash = payload["scene_state_hash"]
    db.commit()
    db.refresh(snapshot)

    return {
        "id": snapshot.id,
        "status": snapshot.status,
        "scene_state_hash": snapshot.scene_state_hash,
    }


# =================================================
# Phase 4.5 — Draft finalization (NON-DESTRUCTIVE)
# =================================================

@router.post("/{snapshot_id}/finalize")
def finalize_draft_snapshot(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    draft = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not draft:
        raise HTTPException(404, "Snapshot not found")

    completed = finalize_snapshot(
        db=db,
        snapshot=draft,
        user=user,
    )

    return {
        "id": completed.id,
        "status": completed.status,
    }


# =================================================
# Tier 6G.1 — Scene Index (READ-ONLY)
# =================================================

@router.get("/{snapshot_id}/scene")
def get_snapshot_scene_index(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    # Read-only deterministic projection
    return build_scene_index(snapshot)
    
    
# =================================================
# Tier 6G.2 — Attach Asset Tool (DRAFT ONLY)
# =================================================

# =================================================
# Tier 6G.2 — Attach Asset Tool (DRAFT ONLY)
# =================================================

@router.post("/{snapshot_id}/tools/attach-asset")
def attach_asset_to_snapshot_scene(
    project_id: int,
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    object_id = str(payload.get("object_id") or "").strip()
    asset_id = payload.get("asset_id")

    if not object_id:
        raise HTTPException(status_code=422, detail="object_id is required")
    if asset_id is None:
        raise HTTPException(status_code=422, detail="asset_id is required")

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(409, "Only draft snapshots can attach assets")

    ownership = snapshot.resolve_ownership(user)
    if ownership == "owned_by_other":
        raise HTTPException(409, "Draft is owned by another user")

    # Load asset
    asset = (
        db.query(Asset)
        .join(ModelRecord)
        .filter(Asset.id == int(asset_id))
        .first()
    )
    if not asset:
        raise HTTPException(404, "Asset not found")

    model = crud.get_model_if_accessible(db, model_id=asset.model_id, user_id=user.id)
    if not model:
        raise HTTPException(403, "No access to asset")

    # Ensure scene structure exists
    if snapshot.body_state is None:
        snapshot.body_state = {}

    scene = snapshot.body_state.get("scene")
    if not isinstance(scene, dict):
        scene = {}
        snapshot.body_state["scene"] = scene

    objects = scene.get("objects")
    if not isinstance(objects, list):
        objects = []
        scene["objects"] = objects

    print("🔍 OBJECTS:", objects)
    print("🔍 TARGET ID:", object_id)

    # =================================================
    # 🔥 FIXED LOGIC (NO MORE BROKEN MATCHING)
    # =================================================

    if not objects:
        # create object if none exists
        found = {
            "id": object_id,
            "kind": str(payload.get("kind") or "vehicle"),
            "name": str(payload.get("name") or asset.filename or object_id),
            "asset_ref": None,
            "transform": {
                "position": {"x": 0, "y": 0, "z": 0},
                "rotation": {"x": 0, "y": 0, "z": 0},
                "scale": {"x": 1, "y": 1, "z": 1},
            },
        }
        objects.append(found)
    else:
        # 🔥 ALWAYS USE FIRST OBJECT (your system = single vehicle)
        found = objects[0]

    # =================================================
    # 🔥 CRITICAL LINE (THIS WAS FAILING BEFORE)
    # =================================================
    found["asset_ref"] = f"asset:{asset.id}"

    print("✅ BOUND ASSET:", found["asset_ref"])

    # Keep deterministic order
    objects.sort(key=lambda x: str((x or {}).get("id") or ""))

    flag_modified(snapshot, "body_state")
    db.commit()
    db.refresh(snapshot)

    return {
        "snapshot_id": snapshot.id,
        "object_id": found["id"],
        "asset_ref": found["asset_ref"],
    }
    

# =================================================
# Tier 7.x — Lock System (REQUIRED)
# =================================================

from app.services.draft_lock_service import acquire_draft_lock

@router.post("/{snapshot_id}/lock")
def acquire_lock(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    # 🔥 CRITICAL FIX — ACTUALLY WRITE LOCK TO DB
    acquire_draft_lock(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    return {
        "state": "owned",
        "snapshot_id": snapshot.id,
        "owner_user_id": user.id,
    }


@router.get("/{snapshot_id}/lock-status")
def get_lock_status(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.owner_user_id == user.id:
        return {"state": "owned"}

    if snapshot.owner_user_id is None:
        return {"state": "unlocked"}

    return {"state": "locked_by_other"}
