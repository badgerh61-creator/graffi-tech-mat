from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services.rendering import render_snapshot
from app.schemas import SnapshotCreate, SnapshotRead
from app.core.config import settings

router = APIRouter(prefix="/projects/{project_id}/snapshots", tags=["Snapshots"])


@router.post("/", response_model=SnapshotRead)
def create_snapshot(
    project_id: int,
    snapshot_in: SnapshotCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 1️⃣ Deterministic cache lookup
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

    # 2️⃣ Create new snapshot record
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

    # 3️⃣ Invoke engine adapter (pure)
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
    return (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

