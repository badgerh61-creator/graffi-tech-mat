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

from app.workspaces.normalize import normalize_snapshots
from app.workspaces.snapshots import get_workspace_snapshots
from app.workspaces.assets import get_workspace_assets

from app.schemas.snapshots import SnapshotRead
from app.schemas.assets import AssetRead


router = APIRouter(
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


# Phase J compatibility alias.
# `/workspace/{id}` is frozen by Phase J tests.
# `/workspaces/{id}` is the canonical path going forward.
# DO NOT diverge behavior between these routes.
@router.get("/workspace/{project_id}")
@router.get("/workspaces/{project_id}")
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

    # Phase J.5 — snapshot assembly (visibility + ordering upstream)
    raw_snapshots = get_workspace_snapshots(
        db=db,
        project_id=project_id,
        include_failed=(
            user.role == "admin" or project.owner_id == user.id
        ),
    )

    normalized_snapshots = normalize_snapshots(raw_snapshots)

    # Phase J.5 — asset assembly (ORDERING ONLY, NO SCOPING)
    assets = get_workspace_assets(db=db)

    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "archived": project.archived_at is not None,
        },
        "capabilities": capabilities,
        "snapshots": [
            SnapshotRead.from_orm(s)
            for s in normalized_snapshots
        ],
        "assets": [
            AssetRead.from_orm(a)
            for a in assets
        ],
        "meta": {
            "snapshot_total": len(raw_snapshots),
            "asset_total": len(assets),
        },
    }

