from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.services.snapshot_state import get_snapshot_state

router = APIRouter(prefix="/studio", tags=["studio"])

@router.get("/snapshots/{snapshot_id}/state")
def read_snapshot_state(snapshot_id: int, user=Depends(get_current_user)):
    return get_snapshot_state(snapshot_id=snapshot_id, user=user)

