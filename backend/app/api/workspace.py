from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
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
    # 🚫 Phase J.4B.1 — NO LOGIC YET
    raise HTTPException(
        status_code=501,
        detail="Workspace endpoint not implemented yet",
    )

