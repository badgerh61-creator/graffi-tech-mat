from fastapi import APIRouter, Depends
from app.api.deps import get_current_user, get_db
from app.services.handoff_service import handoff_draft_ownership

router = APIRouter(prefix="/snapshots")

@router.post("/{snapshot_id}/handoff")
def handoff_snapshot(snapshot_id: int, to_user_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    snapshot = load_snapshot(snapshot_id, db)
    target_user = load_user(to_user_id, db)

    lock = handoff_draft_ownership(
        db=db,
        snapshot=snapshot,
        from_user=user,
        to_user=target_user,
    )

    return {"status": "handed_off", "owner_user_id": lock.user_id}

