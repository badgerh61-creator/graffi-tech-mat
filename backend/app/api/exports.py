# backend/app/api/exports.py

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.models.journal_entry import JournalEntry
from app.models.user import User

router = APIRouter(
    prefix="/exports",
    tags=["exports"],
)

SUPPORTED_EXPORT_TYPES = {
    "image",
    "print",
    "vector",
    "3d",
    "package",
}


@router.post("/requests")
def create_export_request(
    payload: dict,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # ─────────────────────────────────────────────
    # Parse & validate payload
    # ─────────────────────────────────────────────
    project_id = payload.get("project_id")
    snapshot_id = payload.get("snapshot_id")
    export_type = payload.get("export_type")
    options = payload.get("options", {})

    if not project_id or not snapshot_id or not export_type:
        raise HTTPException(status_code=400, detail="Invalid request shape")

    if export_type not in SUPPORTED_EXPORT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported export type")

    # ─────────────────────────────────────────────
    # Phase M.0 / M.1 capability gates (MUST be first)
    # ─────────────────────────────────────────────
    if user.role == "viewer":
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions to request export",
        )

    if not user.is_admin and export_type != "image":
        raise HTTPException(
            status_code=403,
            detail="Export type not permitted",
        )

    # ─────────────────────────────────────────────
    # Project validation
    # ─────────────────────────────────────────────
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=403, detail="Project not accessible")

    if project.archived_at is not None:
        raise HTTPException(status_code=403, detail="Project is archived")

    # ─────────────────────────────────────────────
    # Snapshot validation
    # ─────────────────────────────────────────────
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.id == snapshot_id)
        .first()
    )

    if not snapshot or snapshot.project_id != project.id:
        raise HTTPException(status_code=403, detail="Snapshot not accessible")

    if snapshot.status != SnapshotStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Snapshot not exportable")

    # ─────────────────────────────────────────────
    # Export-type specific validation
    # ─────────────────────────────────────────────
    if export_type == "image" and options:
        if "format" not in options:
            raise HTTPException(status_code=400, detail="Invalid image options")

    # ─────────────────────────────────────────────
    # Create export request (ID only for now)
    # ─────────────────────────────────────────────
    export_request_id = str(uuid4())

    # ─────────────────────────────────────────────
    # Journal intent (schema-safe)
    # ─────────────────────────────────────────────
    db.add(
        JournalEntry(
            project_id=project.id,
            mutation_type="EXPORT_REQUEST",
            type="EXPORT_REQUESTED",
            snapshot_before=snapshot.id,
            snapshot_after=snapshot.id,
            actor_id=user.id,
            actor_user_id=user.id,
        )
    )

    db.commit()

    return {
        "export_request_id": export_request_id,
        "status": "accepted",
    }


@router.get("/health")
def exports_health(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return {"status": "ok"}

