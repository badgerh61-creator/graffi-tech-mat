from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.rendered_snapshot import RenderedSnapshot

from app.services.capabilities import require_capability
from app.services.decor_exterior import (
    apply_exterior_decal_mutation,
    remove_exterior_decal_mutation,
)

from app.api.mutations.decor.schemas import (
    ApplyExteriorDecalPayload,
    RemoveExteriorDecalPayload,
)

# -------------------------------------------------
# ROUTER (MUST BE DEFINED FIRST)
# -------------------------------------------------

router = APIRouter(
    prefix="/mutations/decor/exterior",
    tags=["mutations"],
)

# -------------------------------------------------
# APPLY DECAL
# -------------------------------------------------

@router.post("/apply-decal")
def apply_decal(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: ApplyExteriorDecalPayload,
):
    try:
        require_capability(
            db=db,
            user=user,
            project_id=payload.project_id,
            capability="canDecorateExterior",
        )
    except Exception:
        return JSONResponse(
            status_code=403,
            content={"error": "decor_capability_required"},
        )

    base_snapshot = db.get(RenderedSnapshot, payload.snapshot_base_id)
    if not base_snapshot:
        return JSONResponse(
            status_code=404,
            content={"error": "base_snapshot_not_found"},
        )

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

# -------------------------------------------------
# REMOVE DECAL (PHASE K.1)
# -------------------------------------------------

@router.post("/remove-decal")
def remove_decal(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: RemoveExteriorDecalPayload,
):
    # ---- Capability gate (viewer must fail here)
    try:
        require_capability(
            db=db,
            user=user,
            project_id=payload.project_id,
            capability="canDecorateExterior",
        )
    except Exception:
        return JSONResponse(
            status_code=403,
            content={"error": "decor_capability_required"},
        )

    base_snapshot = db.get(RenderedSnapshot, payload.snapshot_base_id)
    if not base_snapshot:
        return JSONResponse(
            status_code=404,
            content={"error": "base_snapshot_not_found"},
        )

    # ---- Missing decal instance → 404
    decals = (base_snapshot.decor_state or {}).get("decals", [])
    if not any(
        d.get("instance_id") == payload.decal_instance_id
        for d in decals
    ):
        return JSONResponse(
            status_code=404,
            content={"error": "decal_instance_not_found"},
        )

    snapshot = remove_exterior_decal_mutation(
        db=db,
        user_id=user.id,
        project_id=payload.project_id,
        base_snapshot=base_snapshot,
        decal_instance_id=payload.decal_instance_id,
    )

    db.commit()
    return {"snapshot_id": snapshot.id}

