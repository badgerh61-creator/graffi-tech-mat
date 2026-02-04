from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import get_db
from app.api.deps import require_viewer
from app.models.snapshot import Snapshot
from app.models.project import Project

router = APIRouter(prefix="/warehouse", tags=["warehouse"])

@router.get("/projects")
def list_projects(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    return [
    {
        "project_id": p.id,
        "name": p.name,
    }
    for p in db.query(Project).order_by(Project.id).all()
]


@router.get("/projects/{project_id}/snapshots")
def list_project_snapshots(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    # HARD READ-ONLY GUARANTEE
    with db.no_autoflush:
        snapshots = (
            db.query(Snapshot)
            .filter(Snapshot.project_id == project_id)
            .order_by(Snapshot.created_at.asc())
            .all()
        )

    return [
        {
            "snapshot_id": s.id,
            "project_id": s.project_id,
            "status": s.status,
            "created_at": s.created_at.isoformat(),
            "created_by": s.created_by,
            "parent_snapshot_id": s.parent_snapshot_id,
            "engine_version": s.engine_version,
            "has_render": False,
            "has_exports": False,
        }
        for s in snapshots
    ]

