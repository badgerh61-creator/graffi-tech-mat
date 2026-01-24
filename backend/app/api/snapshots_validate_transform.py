from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.constraint_validator import validate_transform
from app.models.rendered_snapshot import RenderedSnapshot

router = APIRouter(
    prefix="/projects/{project_id}/snapshots/{snapshot_id}",
    tags=["snapshots"],
)


@router.post("/validate-transform")
def validate_transform_endpoint(
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

    if snapshot.status != "draft":
        raise HTTPException(409, "Snapshot not draft")

    if user.role not in ("editor", "owner", "admin"):
        raise HTTPException(403, "Insufficient permissions")

    violations = validate_transform(
        snapshot=snapshot,
        target=payload.get("target_id"),
        operation=payload.get("operation"),
        params=payload.get("params", {}),
        constraints=payload.get("constraints", []),
    )

    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }

