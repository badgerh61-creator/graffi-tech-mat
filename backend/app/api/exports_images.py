from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_editor
from app.services.image_exporter import create_image_export
from app.crud.snapshots import get_snapshot_by_id

router = APIRouter(prefix="/exports/images", tags=["exports"])


@router.post("")
def export_image(
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    snapshot = get_snapshot_by_id(db, payload["snapshot_id"])
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    if snapshot.status != "completed":
        raise HTTPException(status_code=409, detail="Snapshot not completed")

    export = create_image_export(
        db=db,
        snapshot=snapshot,
        user=user,
        format=payload["format"],
        resolution=payload["resolution"],
    )

    return {
        "export_id": export.id,
        "status": export.status,
    }

