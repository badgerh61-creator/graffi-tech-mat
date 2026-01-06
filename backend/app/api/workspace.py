"""
PHASE J WORKSPACE CONTRACT (FROZEN)

This endpoint assembles the canonical workspace payload delivered to the editor.

Guarantees:
- Read-only
- Deterministic
- Snapshot-based visual truth
- No scene mutation
- No snapshot mutation
- No engine side effects
- No implicit writes during editor boot

Any write operation MUST go through the Phase I mutation system.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot
from app.models.asset import Asset
from app.models.model import ModelRecord
from app.workspaces.normalize import normalize_snapshots

router = APIRouter(
    prefix="/workspace",
    tags=["Workspace"],
)


@router.get("/{project_id}")
def read_workspace(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # 🧱 Phase J.4B.2 — PROJECT OWNERSHIP ENFORCEMENT (READ-ONLY)
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

    # 🧠 Phase J.4C — CAPABILITY DERIVATION (READ-ONLY)
    is_owner = project.owner_id == user.id

    capabilities = {
        "can_view_assets": is_owner,
        "can_view_snapshots": is_owner,
        "can_edit_project": is_owner,
    }

    # 🧩 Phase J.5 — SNAPSHOT ASSEMBLY + NORMALIZATION (READ-ONLY)
    raw_snapshots = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

    normalized_snapshots = normalize_snapshots(raw_snapshots) if is_owner else {
        "completed": [],
        "failed": [],
        "pending": [],
    }

    # 🧩 Phase J.5 — ASSET ASSEMBLY (DETERMINISTIC ORDER)
    assets = (
        db.query(Asset)
        .join(ModelRecord, Asset.model_id == ModelRecord.id)
        .filter(ModelRecord.owner_id == user.id)
        .order_by(Asset.created_at.desc())
        .all()
    ) if is_owner else []

    return {
        "project": project,
        "snapshots": normalized_snapshots,
        "assets": assets,
        "capabilities": capabilities,
        "meta": {
            "snapshot_total": len(raw_snapshots),
            "asset_total": len(assets),
        },
    }

