from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.asset import Asset
from app.models.model import ModelRecord
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

    # 🧩 Phase J.4B.3 — SNAPSHOT ASSEMBLY (READ-ONLY)
    snapshots = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

    # 🧩 Phase J.4B.4 — ASSET ASSEMBLY (OWNER → MODELS → ASSETS)
    assets = (
        db.query(Asset)
        .join(ModelRecord, Asset.model_id == ModelRecord.id)
        .filter(ModelRecord.owner_id == user.id)
        .order_by(Asset.created_at.desc())
        .all()
    )

    return {
        "project": project,
        "snapshots": snapshots,
        "assets": assets,
    }

