from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.services.capabilities import require_capability
from app.api.deps import get_db, get_current_user
from app.api.mutations.tuning.set_suspension import set_suspension_preset
from app.api.mutations.tuning.set_wheels import set_wheels
from app.api.mutations.tuning.set_engine_tune import set_engine_tune
from app.api.mutations.tuning.set_brakes import set_brakes

router = APIRouter(prefix="/mutations/tuning", tags=["tuning"])


def _require_tuning_capability(db, user, project_id):
    """
    Canonical router-level capability wrapper.
    Normalizes error shape for tests & clients.
    """
    try:
        require_capability(
            db=db,
            user=user,
            project_id=project_id,
            capability="canTune",
        )
    except HTTPException:
        return JSONResponse(
            status_code=403,
            content={
                "error": "tuning_capability_required",
                "detail": "tuning_capability_required",
            },
        )
    return None


@router.post("/set-suspension")
def set_suspension_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = _require_tuning_capability(db, user, payload.get("project_id"))
    if error:
        return error

    return set_suspension_preset(db=db, user=user, payload=payload)


@router.post("/set-wheels")
def set_wheels_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = _require_tuning_capability(db, user, payload.get("project_id"))
    if error:
        return error

    return set_wheels(db=db, user=user, payload=payload)


@router.post("/set-engine-tune")
def set_engine_tune_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = _require_tuning_capability(db, user, payload.get("project_id"))
    if error:
        return error

    return set_engine_tune(db=db, user=user, payload=payload)


@router.post("/set-brakes")
def set_brakes_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = _require_tuning_capability(db, user, payload.get("project_id"))
    if error:
        return error

    return set_brakes(db=db, user=user, payload=payload)

