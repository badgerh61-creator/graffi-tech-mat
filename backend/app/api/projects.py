from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.user import User
from app.schemas import ProjectCreate, ProjectRead
from app import crud

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
        active_snapshot_id=None,  # Phase I invariant
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Phase I: owner-only visibility
    if project.owner_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    return project


# ==================================================
# PHASE I.3 — ACTIVE SNAPSHOT SWITCH (NO JOURNAL)
# ==================================================

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

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Phase I.3 permission gate
    crud.require_project_role(
        db,
        user=user,
        project=project,
        min_role="editor",
    )

    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project.id,
        )
        .first()
    )
    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    if snapshot.status != SnapshotStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail="Only completed snapshots may be activated",
        )

    project.active_snapshot_id = snapshot.id
    db.commit()

    return {
        "status": "ok",
        "project_id": project.id,
        "active_snapshot_id": snapshot.id,
    }

