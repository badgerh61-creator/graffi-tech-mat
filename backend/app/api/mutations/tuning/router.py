from fastapi import APIRouter, Depends
from app.services.capabilities import require_capability

from app.api.deps import get_db, get_current_user
from app.api.mutations.tuning.set_suspension import set_suspension_preset
from app.api.mutations.tuning.set_wheels import set_wheels
from app.api.mutations.tuning.set_engine_tune import set_engine_tune

router = APIRouter(prefix="/mutations/tuning", tags=["tuning"])


@router.post("/set-suspension")
def set_suspension_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    require_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
    )

    return set_suspension_preset(db=db, user=user, payload=payload)


@router.post("/set-wheels")
def set_wheels_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    require_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
    )

    return set_wheels(db=db, user=user, payload=payload)


@router.post("/set-engine-tune")
def set_engine_tune_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    require_capability(
        db=db,
        user=user,
        project_id=payload.get("project_id"),
        capability="canTune",
    )

    return set_engine_tune(db=db, user=user, payload=payload)

