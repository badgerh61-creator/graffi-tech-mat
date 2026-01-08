from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.crud import require_project_role

"""
Public snapshot switching router.

IMPORTANT ARCHITECTURAL RULE:
- Undo / snapshot switching is a PROJECT concern
- It must NOT live under /mutations
- It performs no mutation, only selection of an existing snapshot
"""

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

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    require_project_role(db, user=user, project=project, min_role="editor")

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

    project.active_snapshot_id = snapshot.id
    db.commit()

    return {
        "status": "ok",
        "activeSnapshotId": snapshot.id,
    }

