from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user

from app.models.user import User
from app.models.rendered_snapshot import RenderedSnapshot, SnapshotStatus

from app.services.capabilities import require_capability
from app.services.decor_exterior import (
    apply_exterior_decal_mutation,
    remove_exterior_decal_mutation,
    set_exterior_material_mutation,
    swap_exterior_bodykit_mutation,
)

from app.api.mutations.decor.schemas import (
    ApplyExteriorDecalPayload,
    RemoveExteriorDecalPayload,
)

from app.validation.decor.rules import validate_material

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
# REMOVE DECAL
# -------------------------------------------------

@router.post("/remove-decal")
def remove_decal(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: RemoveExteriorDecalPayload,
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

    decals = (base_snapshot.decor_state or {}).get("decals", [])
    if not any(d.get("instance_id") == payload.decal_instance_id for d in decals):
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


# -------------------------------------------------
# SET MATERIAL (PHASE K.1 — CANONICAL)
# -------------------------------------------------

@router.post("/set-material")
def set_material(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: dict,
):
    project_id = payload.get("project_id")

    try:
        require_capability(
            db=db,
            user=user,
            project_id=project_id,
            capability="canDecorateExterior",
        )
    except Exception:
        return JSONResponse(
            status_code=403,
            content={"error": "decor_capability_required"},
        )

    base_snapshot = db.get(RenderedSnapshot, payload.get("snapshot_base_id"))
    if (
        not base_snapshot
        or base_snapshot.status != SnapshotStatus.COMPLETED
        or base_snapshot.is_obsolete
    ):
        return JSONResponse(
            status_code=409,
            content={"error": "invalid_snapshot_base"},
        )

    panel = payload.get("panel")
    if panel not in (base_snapshot.vehicle_panels or []):
        return JSONResponse(
            status_code=400,
            content={"error": "invalid_target_panel"},
        )

    material = payload.get("material", {})
    ok, _ = validate_material(material.get("parameters", {}))
    if not ok:
        return JSONResponse(
            status_code=400,
            content={"error": "invalid_material_definition"},
        )

    snapshot = set_exterior_material_mutation(
        db=db,
        user_id=user.id,
        project_id=project_id,
        base_snapshot=base_snapshot,
        panel=panel,
        material=material,
    )

    db.commit()
    return {"snapshot_id": snapshot.id}


# -------------------------------------------------
# SWAP BODYKIT (PHASE K.1 — CANONICAL)
# -------------------------------------------------

@router.post("/swap-bodykit")
def swap_bodykit(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: dict,
):
    project_id = payload.get("project_id")

    try:
        require_capability(
            db=db,
            user=user,
            project_id=project_id,
            capability="canDecorateExterior",
        )
    except Exception:
        return JSONResponse(
            status_code=403,
            content={"error": "decor_capability_required"},
        )

    base_snapshot = db.get(RenderedSnapshot, payload.get("snapshot_base_id"))
    if (
        not base_snapshot
        or base_snapshot.status != SnapshotStatus.COMPLETED
        or base_snapshot.is_obsolete
    ):
        return JSONResponse(
            status_code=409,
            content={"error": "invalid_snapshot_base"},
        )

    bodykit_id = payload.get("bodykit_id")
    if not bodykit_id:
        return JSONResponse(
            status_code=404,
            content={"error": "bodykit_not_found"},
        )

    try:
        snapshot = swap_exterior_bodykit_mutation(
            db=db,
            user_id=user.id,
            project_id=project_id,
            base_snapshot=base_snapshot,
            bodykit_id=bodykit_id,
        )
    except KeyError:
        return JSONResponse(
            status_code=404,
            content={"error": "bodykit_not_found"},
        )
    except ValueError:
        return JSONResponse(
            status_code=409,
            content={"error": "bodykit_incompatible"},
        )

    db.commit()
    return {"snapshot_id": snapshot.id}

