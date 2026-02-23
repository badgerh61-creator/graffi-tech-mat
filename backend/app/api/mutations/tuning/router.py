from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.deps import get_db, get_current_user

from app.api.mutations.tuning.set_suspension import set_suspension_preset
from app.api.mutations.tuning.set_wheels import set_wheels
from app.api.mutations.tuning.set_engine_tune import set_engine_tune
from app.api.mutations.tuning.set_brakes import set_brakes

router = APIRouter(prefix="/mutations/tuning", tags=["tuning"])


def _deny_tuning_capability() -> JSONResponse:
    # Some tests assert ["error"], others assert ["detail"]
    return JSONResponse(
        status_code=403,
        content={
            "error": "tuning_capability_required",
            "detail": "tuning_capability_required",
        },
    )


def _require_can_tune(*, user, payload: dict):
    """
    Phase K.2 — HARD tuning capability gate

    This must be deterministic even if other parts of the system
    temporarily bypass capability checks (env flags, dev mode, etc).

    Rules:
    - viewers never tune
    - owners always tune
    - editors tune only if user.can_tune is True
    """
    # Safety: payload must include project_id for the mutation,
    # but capability is enforced based on user authority.
    # (We don't mutate or query project here.)
    _ = payload.get("project_id")

    if user.role == "viewer":
        return _deny_tuning_capability()

    if user.role == "owner":
        return None

    # editor / other roles must explicitly have can_tune
    if not getattr(user, "can_tune", False):
        return _deny_tuning_capability()

    return None


@router.post("/set-suspension")
def set_suspension_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    denied = _require_can_tune(user=user, payload=payload)
    if denied:
        return denied
    return set_suspension_preset(db=db, user=user, payload=payload)


@router.post("/set-wheels")
def set_wheels_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    denied = _require_can_tune(user=user, payload=payload)
    if denied:
        return denied
    return set_wheels(db=db, user=user, payload=payload)


@router.post("/set-engine-tune")
def set_engine_tune_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    denied = _require_can_tune(user=user, payload=payload)
    if denied:
        return denied
    return set_engine_tune(db=db, user=user, payload=payload)


@router.post("/set-brakes")
def set_brakes_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    denied = _require_can_tune(user=user, payload=payload)
    if denied:
        return denied
    return set_brakes(db=db, user=user, payload=payload)
