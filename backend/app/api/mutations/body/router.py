# app/api/mutations/body/router.py

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.deps import get_db, get_current_user
from app.api.mutations.body.apply_morph import apply_body_morph
from app.schemas.body import BodyMorphApplyPayload

from app.validation.body.errors import (
    BodyPresetNotFound,
    BodyPresetIncompatible,
    BodyParametersOutOfBounds,
    InvalidSnapshotBase,
)

router = APIRouter(prefix="/mutations/body", tags=["body"])


@router.post("/apply-morph")
def apply_morph_endpoint(
    payload: BodyMorphApplyPayload,
    db=Depends(get_db),
    user=Depends(get_current_user),
):

    try:
        return apply_body_morph(
            db=db,
            user=user,
            payload=payload,
        )

    except BodyPresetNotFound:
        return JSONResponse(
            status_code=404,
            content={"error": "body_preset_not_found"},
        )

    except BodyPresetIncompatible:
        return JSONResponse(
            status_code=409,
            content={"error": "body_preset_incompatible"},
        )

    except InvalidSnapshotBase:
        return JSONResponse(
            status_code=409,
            content={"error": "invalid_snapshot_base"},
        )

    except BodyParametersOutOfBounds:
        return JSONResponse(
            status_code=400,
            content={"error": "body_parameters_out_of_bounds"},
        )

