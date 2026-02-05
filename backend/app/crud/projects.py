# backend/app/crud/projects.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.models.project import Project


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


def get_projects_accessible_to_user(
    *,
    db: Session,
    user_id: int,
):
    """
    READ-ONLY visibility resolver.

    Ownership-only by design.
    DO NOT introduce membership until a later phase.
    """

    return (
        db.query(Project)
        .filter(Project.owner_id == user_id)
        .all()
    )
