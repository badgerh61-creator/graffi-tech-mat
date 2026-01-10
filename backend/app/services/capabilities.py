from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User


def require_capability(
    *,
    db: Session,
    user: User,
    project_id: int,
    capability: str,
):
    """
    Canonical write-authorization gate.

    RULES:
    - DB is source of truth
    - Roles derive capabilities
    - Endpoints never inspect roles
    """

    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.archived_at is not None:
        raise HTTPException(
            status_code=403,
            detail="decor_capability_required",
        )

    # Admin override
    if user.is_admin:
        return

    # Viewer is ALWAYS read-only
    if user.role == "viewer":
        raise HTTPException(
            status_code=403,
            detail="decor_capability_required",
        )

    # Capability matrix
    if capability == "canDecorateExterior":
        if user.role in {"editor", "owner"}:
            return

    raise HTTPException(
        status_code=403,
        detail="decor_capability_required",
    )

