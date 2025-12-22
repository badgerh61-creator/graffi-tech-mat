from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import get_current_user
from app import crud
from app.services import storage as s3
from app.schemas import ModelCreate
from app.models.model import ModelRecord

router = APIRouter(prefix="/models", tags=["models"])

MODEL_URL_EXPIRES = 300  # seconds


@router.get("/")
def list_models(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        db.query(ModelRecord)
        .filter(ModelRecord.owner_id == user.id)
        .all()
    )


@router.post("/")
def create_model(
    model_in: ModelCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return crud.create_model(
        db,
        model_in,
        owner_id=user.id,
    )


@router.get("/{model_id}")
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    model = (
        db.query(ModelRecord)
        .filter(
            ModelRecord.id == model_id,
            ModelRecord.owner_id == user.id,
        )
        .first()
    )

    if not model:
        raise HTTPException(404, "Model not found")

    return model


@router.get("/{model_id}/url")
def get_model_glb_url(
    model_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    model = (
        db.query(ModelRecord)
        .filter(
            ModelRecord.id == model_id,
            ModelRecord.owner_id == user.id,
        )
        .first()
    )

    if not model:
        raise HTTPException(404, "Model not found")

    for asset in model.assets:
        if asset.filename.lower().endswith(".glb"):
            return {
                "url": s3.get_presigned_url(
                    asset.s3_key,
                    expires_seconds=MODEL_URL_EXPIRES,
                ),
                "expires_in": MODEL_URL_EXPIRES,
                "asset_id": asset.id,
            }

    raise HTTPException(404, "No GLB asset attached")

