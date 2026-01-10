# app/api/mutations/public_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services.capabilities import require_capability

public_router = APIRouter()

@public_router.post("/projects/{project_id}/snapshots/active")
def set_active_snapshot_public(
    project_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot_id = payload.get("snapshot_id")
    if not snapshot_id:
        raise HTTPException(status_code=400, detail="snapshot_id required")

    require_capability(
        db=db,
        user=user,
        project_id=project_id,
        capability="canDecorateExterior",
    )

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
            RenderedSnapshot.status == SnapshotStatus.COMPLETED,
        )
        .first()
    )
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    project = db.get(Project, project_id)
    project.active_snapshot_id = snapshot.id
    db.commit()

    return {
        "status": "ok",
        "activeSnapshotId": snapshot.id,
    }

