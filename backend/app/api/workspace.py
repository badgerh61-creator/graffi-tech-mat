from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.schemas import WorkspaceRead

router = APIRouter(
    prefix="/workspace",
    tags=["Workspace"],
)


@router.get("/{project_id}", response_model=WorkspaceRead)
def read_workspace(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🧱 Phase J.4B.2 — PROJECT OWNERSHIP ENFORCEMENT
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.owner_id == user.id,
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    # 🚫 Phase J.4B.2 — STILL NO AGGREGATION
    raise HTTPException(
        status_code=501,
        detail="Workspace data not assembled yet",
    )

