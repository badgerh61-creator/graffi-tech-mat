from fastapi import APIRouter, Depends

from app.api.deps import get_db, get_current_user
from app.api.mutations.tuning.set_suspension import set_suspension_preset

router = APIRouter(prefix="/mutations/tuning", tags=["tuning"])


@router.post("/set-suspension")
def set_suspension_endpoint(
    payload: dict,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    return set_suspension_preset(db=db, user=user, payload=payload)

