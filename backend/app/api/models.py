# =========================================
# Graffi-Tech-Mat — Models API
# Phase 4.6 — TUPLE-SAFE NORMALIZATION FIX
# =========================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_viewer, require_editor
from app import crud
from app.services import storage as s3
from app.schemas import ModelCreate, ModelRead
from app.models.asset import AssetStatus
from app.models.model_permission import ModelPermission

router = APIRouter(prefix="/models", tags=["models"])

MODEL_URL_EXPIRES = 300


@router.get("/", response_model=list[ModelRead])
def list_models(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    raw_models = crud.get_models_accessible_to_user(db, user.id)

    results = []

    for row in raw_models:
        # 🔧 FIX: unwrap tuple if needed
        model = row[0] if isinstance(row, tuple) else row

        # 🔐 Resolve role
        role = "viewer"

        owner = crud.get_model_owner(db, model)
        if owner["type"] == "user" and owner["id"] == user.id:
            role = "owner"
        else:
            perm = (
                db.query(ModelPermission)
                .filter(
                    ModelPermission.model_id == model.id,
                    ModelPermission.user_id == user.id,
                )
                .first()
            )
            if perm:
                role = perm.role

        results.append(
            ModelRead(
                id=model.id,
                name=model.name,
                description=model.description,
                owner_id=model.owner_id,
                created_at=model.created_at,
                role=role,
                assets=model.assets,
            )
        )

    return results

