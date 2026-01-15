# app/services/capabilities.py

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
    Canonical write-authorization gate (Phase S).
    All mutation-level authorization flows through this function.
    """

    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="project_not_found")

    # 🔒 Archived projects are always read-only
    if project.archived_at is not None:
        raise HTTPException(status_code=403, detail="project_archived")

    # 🔑 Admin override
    if user.is_admin:
        return

    # 👁 Viewer is always read-only
    if user.role == "viewer":
        raise HTTPException(status_code=403, detail="capability_required")

    # =========================
    # Capability matrix
    # =========================

    # Phase K.1 — exterior decor
    if capability == "canDecorateExterior":
        if user.role in {"editor", "owner"}:
            return

    # Phase K.2 — tuning
    if capability == "canTune":
        if user.role == "owner" or getattr(user, "can_tune", False):
            return

    # Phase K.3 — body transforms (OWNER ONLY)
    if capability == "body_edit":
        if user.role == "owner":
            return

    # ❌ Capability not satisfied
    raise HTTPException(status_code=403, detail="capability_required")

