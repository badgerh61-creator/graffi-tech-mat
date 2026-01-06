from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
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


@router.post("/", response_model=SnapshotRead)
def create_snapshot(
    project_id: int,
    snapshot_in: SnapshotCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase J / Phase I invariant:
    - Snapshot creation is deterministic
    - No implicit project state mutation
    - Snapshot activation is NOT handled here
    """

    existing = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.scene_state_hash == snapshot_in.scene_state_hash,
            RenderedSnapshot.render_profile == snapshot_in.render_profile,
            RenderedSnapshot.engine_version == settings.ENGINE_VERSION,
            RenderedSnapshot.status == SnapshotStatus.COMPLETED,
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
        status=SnapshotStatus.RUNNING,
        created_by=user.id,
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    try:
        image_url = render_snapshot({}, snapshot.render_profile)
        snapshot.image_url = image_url
        snapshot.status = SnapshotStatus.COMPLETED
    except Exception as e:
        snapshot.status = SnapshotStatus.FAILED
        snapshot.error_message = str(e)

    db.commit()
    db.refresh(snapshot)
    return snapshot


@router.get("/", response_model=list[SnapshotRead])
def list_snapshots(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase J invariant:
    - Read-only
    - Deterministic ordering
    """
    return (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )


# -------------------------------------------------
# Global snapshot mutations (Phase I)
# -------------------------------------------------

mutation_router = APIRouter(
    tags=["Snapshot Mutations"],
)


@mutation_router.post(
    "/snapshots/{snapshot_id}/mutations/invalidate",
    status_code=200,
)
def invalidate_snapshot(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Phase I.4 — Snapshot invalidation

    Rules:
    - Only COMPLETED snapshots may be invalidated
    - No deletion
    - Status transitions are explicit and irreversible
    """

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )

    if not snapshot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snapshot not found",
        )

    if snapshot.status != SnapshotStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot invalidate snapshot with status '{snapshot.status}'",
        )

    snapshot.status = "obsolete" 
    db.commit()
    db.refresh(snapshot)

    return {
        "snapshot_id": snapshot.id,
        "status": snapshot.status,
    }

