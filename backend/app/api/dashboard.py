from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_viewer
from app.models.project import Project
from app.models.snapshot import Snapshot
from app.models.audit import AuditLog
from app import crud

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/projects")
def list_dashboard_projects(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    projects = crud.get_projects_accessible_to_user(
        db=db,
        user_id=user.id,
    )

    results = []
    for p in projects:
        snapshot_count = (
            db.query(Snapshot)
            .filter(Snapshot.project_id == p.id)
            .count()
        )

        last_activity = (
            db.query(AuditLog)
            .filter(
                AuditLog.resource_type == "project",
                AuditLog.resource_id == p.id,
            )
            .order_by(AuditLog.created_at.desc())
            .first()
        )

        results.append(
            {
                "project_id": p.id,
                "name": p.name,
                "created_at": p.created_at.isoformat(),
                "owner_id": p.owner_id,
                "snapshot_count": snapshot_count,
                "last_activity_at": (
                    last_activity.created_at.isoformat()
                    if last_activity else None
                ),
            }
        )

    return results


@router.get("/activity")
def list_dashboard_activity(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    projects = crud.get_projects_accessible_to_user(
        db=db,
        user_id=user.id,
    )

    project_ids = [p.id for p in projects]

    events = (
        db.query(AuditLog)
        .filter(
            AuditLog.resource_type == "project",
            AuditLog.resource_id.in_(project_ids),
        )
        .order_by(AuditLog.created_at.desc())
        .limit(50)
        .all()
    )

    return [
        {
            "action": e.action,
            "actor_user_id": e.user_id,
            "resource_type": e.resource_type,
            "resource_id": e.resource_id,
            "created_at": e.created_at.isoformat(),
            "summary": e.summary,
        }
        for e in events
    ]

