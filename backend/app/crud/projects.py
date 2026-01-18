# backend/app/crud/projects.py

from sqlalchemy.orm import Session

from app.models.user import User


def require_project_role(
    db: Session,
    *,
    user: User,
    project,
    min_role: str,
):
    """
    Phase I.3:
    Simple project ownership enforcement.
    Expandable later to org/project roles.
    """

    if user.is_admin:
        return

    if project.owner_id == user.id:
        return

    raise PermissionError("Insufficient project permissions")        

