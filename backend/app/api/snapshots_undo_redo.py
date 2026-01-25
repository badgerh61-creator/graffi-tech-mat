from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot
from app.services.snapshot_navigation import undo_snapshot, redo_snapshot

router = APIRouter(prefix="/projects/{project_id}/snapshots", tags=["snapshots"])

@router.post("/{snapshot_id}/undo")
def undo(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snap = db.query(RenderedSnapshot).filter_by(
        id=snapshot_id,
        project_id=project_id,
    ).first()

    if not snap:
        raise HTTPException(404, "Snapshot not found")

    target = undo_snapshot(db=db, snapshot=snap, user=user)

    return {"active_snapshot_id": target.id}

@router.post("/{snapshot_id}/redo")
def redo(
    project_id: int,
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snap = db.query(RenderedSnapshot).filter_by(
        id=snapshot_id,
        project_id=project_id,
    ).first()

    if not snap:
        raise HTTPException(404, "Snapshot not found")

    target = redo_snapshot(db=db, snapshot=snap, user=user)

    return {"active_snapshot_id": target.id}

