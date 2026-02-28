# backend/app/api/draft_lock_status.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user

router = APIRouter(prefix="/snapshots", tags=["draft-lock"])


def _get_snapshot_model():
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot
        return Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore
        return Snapshot


@router.get("/{snapshot_id}/lock-status")
def lock_status_endpoint(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    user_id = getattr(user, "id", None)
    if not user_id:
        raise HTTPException(401, "Not authenticated")

    Snapshot = _get_snapshot_model()
    snap = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snap:
        raise HTTPException(404, "Snapshot not found")

    # Only drafts are lockable. For completed snapshots, lock is irrelevant.
    if getattr(snap, "status", None) != "draft":
        return {"state": "missing"}

    # ✅ Use your existing lock reader
    try:
        from app.services.draft_lock_service import get_draft_lock  # <-- you have this
        lock = get_draft_lock(db=db, snapshot=snap)
        if lock is None:
            return {"state": "missing"}
        if int(lock.user_id) == int(user_id):
            return {"state": "owned", "owner_id": int(lock.user_id)}
        return {"state": "taken", "owner_id": int(lock.user_id)}
    except Exception:
        return {"state": "unknown"}
