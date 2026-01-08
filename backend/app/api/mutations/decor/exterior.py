from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.rendered_snapshot import RenderedSnapshot

from app.services.capabilities import require_capability
from app.services.decor_exterior import apply_exterior_decal_mutation

from app.api.mutations.decor.schemas import ApplyExteriorDecalPayload
from app.validation.decor.exterior import validate_apply_decal
from app.validation.decor.errors import DecorValidationError


router = APIRouter(
    prefix="/mutations/decor/exterior",
    tags=["mutations"],
)


@router.post("/apply-decal")
def apply_decal(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: ApplyExteriorDecalPayload,
):
    # ---------------------------------------------------------
    # Capability gate (Phase K.0)
    # ---------------------------------------------------------
    require_capability(
        db=db,
        user=user,
        project_id=payload.project_id,
        capability="canDecorateExterior",
    )

    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    base_snapshot = (
        db.query(RenderedSnapshot)
        .filter(
            RenderedSnapshot.id == payload.snapshot_base_id,
            RenderedSnapshot.project_id == payload.project_id,
        )
        .first()
    )
    if not base_snapshot:
        raise HTTPException(status_code=404, detail="Base snapshot not found")

    # ---------------------------------------------------------
    # Canonical validation (LAW)
    # ---------------------------------------------------------
    try:
        validate_apply_decal(
            capabilities={"canDecorateExterior": True},
            snapshot=base_snapshot,
            decal=type("Decal", (), {"is_exterior": True})(),  # placeholder
            target=payload.target,
        )
    except DecorValidationError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"error": e.error_code, "message": e.message},
        )

    # ---------------------------------------------------------
    # Delegate mutation (single source of truth)
    # ---------------------------------------------------------
    snapshot = apply_exterior_decal_mutation(
        db=db,
        user_id=user.id,
        project_id=payload.project_id,
        base_snapshot=base_snapshot,
        decal_id=payload.decal_id,
        target=payload.target,
    )

    db.commit()
    return {"snapshot_id": snapshot.id}

