from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.snapshot_finalize import finalize_snapshot
from app.services.snapshot_drafts import (
    create_draft_from_completed,
    autosave_draft,
)
from app.services.snapshot_invalidation import invalidate_snapshot
from app import crud

router = APIRouter(prefix="/snapshots", tags=["snapshots-legacy"])


# -----------------------------
# CREATE DRAFT (legacy)
# -----------------------------
@router.post("/{snapshot_id}/draft")
def create_draft(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = crud.get_snapshot_by_id(db, snapshot_id)
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    return create_draft_from_completed(
        db=db,
        snapshot=snapshot,
        user=user,
    )


# -----------------------------
# AUTOSAVE DRAFT (legacy)
# POST + PUT REQUIRED
# -----------------------------
@router.post("/{snapshot_id}/autosave")
@router.put("/{snapshot_id}/autosave")
def autosave(
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = crud.get_snapshot_by_id(db, snapshot_id)
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    return autosave_draft(
        db=db,
        snapshot=snapshot,
        new_state_hash=payload["scene_state_hash"],
        user=user,
    )


# -----------------------------
# FINALIZE (legacy)
# -----------------------------
@router.post("/{snapshot_id}/finalize")
def finalize(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = crud.get_snapshot_by_id(db, snapshot_id)
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    completed = finalize_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )

    return {
        "status": completed.status,
        "snapshot_id": completed.id,
    }


# -----------------------------
# INVALIDATE (legacy)
# -----------------------------
@router.post("/{snapshot_id}/invalidate")
def invalidate(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = crud.get_snapshot_by_id(db, snapshot_id)
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    return invalidate_snapshot(
        db=db,
        snapshot=snapshot,
        user=user,
    )


# -----------------------------
# AUTOSAVE DRAFT (legacy)
# POST + PUT + PATCH REQUIRED
# -----------------------------
@router.post("/{snapshot_id}/autosave")
@router.put("/{snapshot_id}/autosave")
@router.patch("/{snapshot_id}/autosave")   # ✅ ADD THIS
def autosave(
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = crud.get_snapshot_by_id(db, snapshot_id)
    if snapshot is None:
        raise HTTPException(404, "Snapshot not found")

    return autosave_draft(
        db=db,
        snapshot=snapshot,
        new_state_hash=payload["scene_state_hash"],
        user=user,
    )

