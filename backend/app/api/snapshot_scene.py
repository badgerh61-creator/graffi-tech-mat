from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.rendered_snapshot import RenderedSnapshot
from app.services.scene_index_service import build_scene_index

router = APIRouter(prefix="/snapshots", tags=["snapshot-scene"])


@router.get("/{snapshot_id}/scene")
def get_snapshot_scene(snapshot_id: int, db: Session = Depends(get_db)):
    """
    Tier 6G.13 — Scene Read API

    Converts snapshot → viewer-ready scene index
    """

    snapshot = db.query(RenderedSnapshot).filter(
        RenderedSnapshot.id == snapshot_id
    ).first()

    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    return build_scene_index(snapshot)
    
    
@router.get("")
def list_snapshots(project_id: int, db: Session = Depends(get_db)):
    """
    List snapshots for a project (latest first)
    """
    snaps = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.id.desc())
        .all()
    )

    return [
        {
            "id": s.id,
            "status": s.status,
            "created_at": str(s.created_at),
        }
        for s in snaps
    ]
