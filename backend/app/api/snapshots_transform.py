from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.snapshot_mutations import apply_transform
from app import crud

router = APIRouter(
    prefix="/projects/{project_id}/snapshots",
    tags=["snapshots-transform"],
)


@router.post("/{snapshot_id}/transform")
def transform_snapshot(
    project_id: int,
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🔐 Permission
    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    snapshot = crud.get_snapshot_by_id(db, snapshot_id)
    if snapshot is None or snapshot.project_id != project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    new_snapshot = apply_transform(
        db=db,
        snapshot=snapshot,
        user=user,
        operation=payload.get("operation"),
        target_id=payload.get("target_id"),
        params=payload.get("params", {}),
    )

    return {
        "snapshot_id": new_snapshot.id,
        "status": "applied",
    }
