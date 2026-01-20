from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user, require_editor
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.schemas import SnapshotCreate, SnapshotRead
from app.services.rendering import render_snapshot
from app.core.config import settings

# -------------------------------------------------
# Project-scoped snapshot routes (Phase J)
# -------------------------------------------------

router = APIRouter(
    prefix="/projects/{project_id}/snapshots",
    tags=["Snapshots"],
)

@router.get("/", response_model=list[SnapshotRead])
def list_snapshots(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase 3 — Read-only snapshot listing
    - Returns ALL snapshots for project
    - Frontend decides which is active
    """
    snapshots = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

    return snapshots


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


# -------------------------------------------------
# Snapshot mutations
# -------------------------------------------------

mutation_router = APIRouter(tags=["Snapshot Mutations"])


@mutation_router.post("/snapshots/{snapshot_id}/mutations/invalidate")
def invalidate_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = db.query(RenderedSnapshot).filter_by(id=snapshot_id).first()

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    if snapshot.status != SnapshotStatus.COMPLETED.value:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Cannot invalidate snapshot with status '{snapshot.status}'",
        )

    snapshot.status = SnapshotStatus.OBSOLETE.value
    db.commit()
    return {"snapshot_id": snapshot.id, "status": snapshot.status}


@mutation_router.post("/snapshots/{snapshot_id}/finalize")
def finalize_draft_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    draft = (
        db.query(RenderedSnapshot)
        .filter_by(id=snapshot_id)
        .first()
    )

    if not draft:
        raise HTTPException(404, "Snapshot not found")

    if draft.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Only draft snapshots can be finalized",
        )

    # 🔒 Ensure only one draft existed (invariant)
    parent = (
        db.query(RenderedSnapshot)
        .filter_by(id=draft.parent_snapshot_id)
        .first()
    )

    if not parent:
        raise HTTPException(409, "Parent snapshot missing")

    # Promote draft → completed
    draft.status = SnapshotStatus.COMPLETED.value
    draft.parent_snapshot_id = None

    db.commit()
    db.refresh(draft)

    return {
        "id": draft.id,
        "status": draft.status,
    }


# -------------------------------------------------
# Phase 4.1 — Draft Snapshot
# -------------------------------------------------

@mutation_router.post("/snapshots/{snapshot_id}/draft")
def create_draft_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    snapshot = db.query(RenderedSnapshot).filter_by(id=snapshot_id).first()

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
            RenderedSnapshot.project_id == snapshot.project_id,
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


# -------------------------------------------------
# Phase 4.3 — Draft Autosave
# -------------------------------------------------

@mutation_router.patch("/snapshots/{snapshot_id}/autosave")
def autosave_draft_snapshot(
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    """
    Phase 4.3
    - Autosave overwrites the SAME draft snapshot
    - No rendering
    - No status change
    """

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
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

