from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot

router = APIRouter(prefix="/snapshots", tags=["tuning-read"])


@router.get("/{snapshot_id}/tuning")
def get_tuning_state(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = db.query(RenderedSnapshot).get(snapshot_id)

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    return snapshot.tuning_state or {
        "engine": {},
        "suspension": {},
        "wheels": {},
        "paint_layers": [],
        "metrics": {},
    }

