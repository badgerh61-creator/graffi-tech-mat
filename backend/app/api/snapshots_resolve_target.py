from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus
from app.services.selection_resolver import resolve_selection

router = APIRouter(
    prefix="/projects/{project_id}/snapshots",
    tags=["snapshots"],
)


@router.post("/{snapshot_id}/resolve-target")
def resolve_target(
    project_id: int,
    snapshot_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == snapshot_id,
            RenderedSnapshot.project_id == project_id,
        )
        .first()
    )

    if not snapshot:
        raise HTTPException(404, "Snapshot not found")

    # Phase 5.2 invariant: only DRAFT snapshots are editable
    if snapshot.status != SnapshotStatus.DRAFT.value:
        raise HTTPException(409, "Snapshot not editable")

    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403, "Insufficient permissions")

    try:
        return resolve_selection(
            snapshot=snapshot,
            selection_type=payload["selection_type"],
            selection_id=payload["selection_id"],
        )
    except KeyError:
        raise HTTPException(404, "Selection not found")
    except PermissionError as e:
        raise HTTPException(403, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))

