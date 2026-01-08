from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.project import Project


def require_capability(
    *,
    db: Session,
    user: User,
    project_id: int,
    capability: str,
):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.archived_at is not None:
        raise HTTPException(status_code=403, detail="Project is archived")

    # Admin override
    if user.is_admin:
        return

    # Viewer: never allowed
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    if capability == "canDecorateExterior":
        if user.role not in {"editor", "owner"}:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return

    raise HTTPException(
        status_code=403,
        detail=f"Capability {capability} not granted",
    )

