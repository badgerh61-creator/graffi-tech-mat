"""
PHASE J WORKSPACE CONTRACT (FROZEN)
PHASE K.0 CAPABILITY EXTENSION (FROZEN)

Canonical workspace payload.

Guarantees:
- Read-only
- Deterministic
- Snapshot-based visual truth
- No scene mutation
- No snapshot mutation
- No engine side effects
- No implicit writes during editor boot

Phase K.0:
- Server-derived write capabilities
- Role-based authority (NO client override)
- Archived project hard stop

Any write operation MUST go through Phase I mutations.
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
    prefix="/workspaces",
    tags=["Workspace"],
)


def derive_capabilities(user, project):
    """
    Phase K.0 — Authoritative write capability gate.
    Role-based only. Client input ignored.
    """

    capabilities = {
        "canDecorateExterior": False,
        "canDecorateInterior": False,
        "canTuneParameters": False,
        "canModifyBody": False,
        "canOverrideValidation": False,
    }

    # Archived project → absolute lock
    if project.archived_at is not None:
        return capabilities

    role = getattr(user, "role", None)

    # ADMIN → full authority
    if role == "admin":
        return {key: True for key in capabilities}

    # EDITOR → limited write
    if role == "editor":
        capabilities.update({
            "canDecorateExterior": True,
            "canDecorateInterior": True,
            "canTuneParameters": True,
        })
        return capabilities

    # VIEWER / fallback → read-only
    return capabilities

@router.get("/{project_id}")
def read_workspace(
    project_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Assemble deterministic, read-only workspace payload.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Phase K.0 — authoritative capabilities
    capabilities = derive_capabilities(user, project)

    # Phase J — snapshot assembly
    raw_snapshots = (
        db.query(RenderedSnapshot)
        .filter(RenderedSnapshot.project_id == project_id)
        .order_by(RenderedSnapshot.created_at.desc())
        .all()
    )

    if user.role == "admin" or project.owner_id == user.id:
        normalized_snapshots = normalize_snapshots(raw_snapshots)
    else:
        normalized_snapshots = {
            "completed": [],
            "failed": [],
            "pending": [],
        }

    # Phase J — asset assembly
    assets = (
        db.query(Asset)
        .join(ModelRecord, Asset.model_id == ModelRecord.id)
        .filter(ModelRecord.owner_id == user.id)
        .order_by(Asset.created_at.desc())
        .all()
    )

    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "archived": project.archived_at is not None,
        },
        "capabilities": capabilities,
        "snapshots": normalized_snapshots,
        "assets": assets,
        "meta": {
            "snapshot_total": len(raw_snapshots),
            "asset_total": len(assets),
        },
    }

