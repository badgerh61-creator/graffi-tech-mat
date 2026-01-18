from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.mutation_journal import MutationJournal
from app.models.user import User
from app.schemas import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = Project(
        name=project_in.name,
        owner_id=user.id,
        active_snapshot_id=None,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}/active-snapshot")
def set_active_snapshot(
    project_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    snapshot_id = payload.get("snapshot_id")
    if not snapshot_id:
        raise HTTPException(status_code=400, detail="snapshot_id required")

    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="Forbidden")

    snapshot = db.get(RenderedSnapshot, snapshot_id)
    if not snapshot or snapshot.project_id != project.id:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    if snapshot.status != SnapshotStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Only completed snapshots may be activated",
        )

    project.active_snapshot_id = snapshot.id
    db.commit()
    return {"status": "ok"}


@router.post("/{project_id}/mutations/rename")
def rename_project(
    project_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.archived_at is not None:
        raise HTTPException(status_code=403, detail="Project is archived")

    if user.role not in ("owner", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    new_name = payload.get("name")
    if not new_name:
        raise HTTPException(status_code=400, detail="name required")

    old_name = project.name
    project.name = new_name

    journal = MutationJournal(
        intent_type="rename",
        target_type="project",
        target_id=project.id,
        before_state={"name": old_name},
        after_state={"name": new_name},
        issued_by_user_id=user.id,
        reason="Phase I.5 project rename",
    )

    db.add(journal)
    db.commit()
    return {"status": "ok"}


@router.post("/{project_id}/mutations/archive")
def archive_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.archived_at is not None:
        raise HTTPException(status_code=409, detail="Project already archived")

    if user.role not in ("owner", "admin"):
        raise HTTPException(status_code=403, detail="Forbidden")

    archived_at = datetime.utcnow()
    project.archived_at = archived_at

    journal = MutationJournal(
        intent_type="archive",
        target_type="project",
        target_id=project.id,
        before_state={"archived_at": None},
        after_state={"archived_at": archived_at.isoformat()},
        issued_by_user_id=user.id,
        reason="Phase I.5 project archive",
    )

    db.add(journal)
    db.commit()
    return {"status": "ok"}

