from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot

router = APIRouter(tags=["SnapshotHistory"])

@router.get("/snapshots/{snapshot_id}/history")
def get_snapshot_history(
    snapshot_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # NOTE: if you have model-level access checks, enforce them here.
    cur = db.query(RenderedSnapshot).filter(RenderedSnapshot.id == snapshot_id).first()
    if not cur:
        raise HTTPException(404, "Snapshot not found")

    nodes = []
    visited = set()

    # walk parent chain: current -> ... -> root
    it = cur
    while it and it.id not in visited:
        visited.add(it.id)

        # children (branches) deterministic
        children = (
            db.query(RenderedSnapshot.id)
            .filter(RenderedSnapshot.parent_snapshot_id == it.id)
            .order_by(RenderedSnapshot.id.asc())
            .all()
        )
        children_ids = [cid for (cid,) in children]

        nodes.append(
            {
                "id": it.id,
                "parent_snapshot_id": it.parent_snapshot_id,
                "children_ids": children_ids,
            }
        )
        it = it.parent_snapshot

    return {
        "snapshot_id": cur.id,
        "has_parent_links": True,
        "nodes": nodes,  # current -> parent -> ... -> root
    }
