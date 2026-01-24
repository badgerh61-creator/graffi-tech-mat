from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.snapshot_invalidation import invalidate_snapshot
from app import crud

router = APIRouter(
    prefix="/snapshots/{snapshot_id}/mutations",
    tags=["snapshot-mutations"],
)


@router.post("/invalidate")
def invalidate_snapshot_mutation(
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

