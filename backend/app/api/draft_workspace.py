from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.draft_workspace_service import start_edit, complete_draft, discard_draft

router = APIRouter(prefix="/snapshots", tags=["draft-workspace"])


def _get_snapshot_model():
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot
        return Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore
        return Snapshot


@router.post("/{snapshot_id}/start-edit")
def start_edit_endpoint(snapshot_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    Snapshot = _get_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    draft_id = start_edit(db=db, snapshot=snap, user=user)
    return {"mode": "edit", "draft_snapshot_id": int(draft_id)}


@router.post("/{snapshot_id}/complete-draft")
def complete_draft_endpoint(snapshot_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    Snapshot = _get_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    completed_id = complete_draft(db=db, snapshot=snap, user=user)
    return {"mode": "read", "completed_snapshot_id": int(completed_id)}


@router.post("/{snapshot_id}/discard-draft")
def discard_draft_endpoint(snapshot_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    Snapshot = _get_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    parent_id = discard_draft(db=db, snapshot=snap, user=user)
    return {"mode": "read", "parent_snapshot_id": int(parent_id)}
