from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.reference_frames import compute_reference_frames_for_snapshot

router = APIRouter(prefix="/snapshots", tags=["reference-frames"])


@router.get("/{snapshot_id}/reference-frames")
def get_reference_frames(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        from app.models.rendered_snapshot import RenderedSnapshot as Snapshot
    except Exception:
        from app.models.snapshot import Snapshot  # type: ignore

    snapshot = db.query(Snapshot).filter(Snapshot.id == snapshot_id).first()
    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    # Optional access-control hook (additive safe)
    try:
        from app import crud
        if hasattr(crud, "get_snapshot_if_accessible"):
            ok = crud.get_snapshot_if_accessible(db, snapshot_id=snapshot_id, user_id=user.id)
            if not ok:
                raise HTTPException(403, "No access to snapshot")
    except HTTPException:
        raise
    except Exception:
        pass

    return compute_reference_frames_for_snapshot(snapshot=snapshot)
