from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_db
from app.services.draft_lock_service import (
    acquire_draft_lock,
    release_draft_lock,
)

router = APIRouter(prefix="/snapshots")

@router.post("/{snapshot_id}/lock")
def lock_snapshot(snapshot_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    snapshot = load_snapshot(snapshot_id, db)
    acquire_draft_lock(db=db, snapshot=snapshot, user=user)
    return {"status": "locked"}

@router.post("/{snapshot_id}/unlock")
def unlock_snapshot(snapshot_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    snapshot = load_snapshot(snapshot_id, db)
    release_draft_lock(db=db, snapshot=snapshot, user=user)
    return {"status": "unlocked"}

