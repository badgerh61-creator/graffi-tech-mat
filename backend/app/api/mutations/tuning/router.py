from fastapi import APIRouter, Depends

from app.api.deps import get_db, get_current_user
from app.api.guards import require_project_capability

from app.api.mutations.tuning.set_suspension import set_suspension_preset
from app.api.mutations.tuning.set_wheels import set_wheels
from app.api.mutations.tuning.set_engine_tune import set_engine_tune
from app.api.mutations.tuning.set_brakes import set_brakes

router = APIRouter(prefix="/mutations/tuning", tags=["tuning"])


@router.post("/set-suspension")
def set_suspension_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = require_project_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
        error_code="tuning_capability_required",
    )
    if error:
        return error

    return set_suspension_preset(db=db, user=user, payload=payload)


@router.post("/set-wheels")
def set_wheels_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = require_project_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
        error_code="tuning_capability_required",
    )
    if error:
        return error

    return set_wheels(db=db, user=user, payload=payload)


@router.post("/set-engine-tune")
def set_engine_tune_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = require_project_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
        error_code="tuning_capability_required",
    )
    if error:
        return error

    return set_engine_tune(db=db, user=user, payload=payload)


@router.post("/set-brakes")
def set_brakes_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    error = require_project_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
        error_code="tuning_capability_required",
    )
    if error:
        return error

    return set_brakes(db=db, user=user, payload=payload)

