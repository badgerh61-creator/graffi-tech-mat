from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_viewer, require_editor
from app import crud
from app.services import storage as s3
from app.services import audit
from app.schemas import ModelCreate

router = APIRouter(prefix="/models", tags=["models"])

MODEL_URL_EXPIRES = 300


# =========================
# LIST MODELS
# =========================

@router.get("/")
def list_models(db: Session = Depends(get_db), user=Depends(require_viewer)):
    return crud.get_models_accessible_to_user(db, user.id)


# =========================
# CREATE MODEL (AUDITED)
# =========================

@router.post("/")
def create_model(
    model_in: ModelCreate,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    model = crud.create_model(db, model_in, owner_id=user.id)

    audit.log_event(
        db,
        user_id=user.id,
        action="model.create",
        resource_type="model",
        resource_id=model.id,
        extra={
            "name": model.name,
        },
    )

    return model


# =========================
# GET MODEL
# =========================

@router.get("/{model_id}")
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    model = crud.get_model_if_accessible(
        db,
        model_id=model_id,
        user_id=user.id,
    )
    if not model:
        raise HTTPException(404, "Model not found or no access")
    return model


# =========================
# GET MODEL URL (HARDENED)
# =========================

@router.get("/{model_id}/url")
def get_model_glb_url(
    model_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    model = crud.get_model_if_accessible(
        db,
        model_id=model_id,
        user_id=user.id,
    )
    if not model:
        raise HTTPException(404, "Model not found or no access")

    for asset in model.assets:
        if asset.filename.lower().endswith(".glb"):
            try:
                return {
                    "url": s3.get_presigned_url(
                        asset.s3_key,
                        expires_seconds=MODEL_URL_EXPIRES,
                    ),
                    "expires_in": MODEL_URL_EXPIRES,
                    "asset_id": asset.id,
                }
            except FileNotFoundError:
                raise HTTPException(
                    status_code=404,
                    detail="Model file missing from storage",
                )
            except Exception:
                raise HTTPException(
                    status_code=503,
                    detail="Storage service unavailable",
                )

    raise HTTPException(404, "No GLB asset attached")


# =========================
# COLLABORATION (PHASE 2)
# =========================

@router.get("/{model_id}/collaborators")
def list_collaborators(
    model_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(404, "Model not found")

    try:
        crud.require_model_role(
            db,
            user=user,
            model=model,
            min_role="viewer",
        )
    except PermissionError:
        raise HTTPException(403, "No access")

    return crud.list_model_collaborators(db, model_id)


# =========================
# ADD COLLABORATOR (AUDITED)
# =========================

@router.post("/{model_id}/collaborators")
def add_collaborator(
    model_id: int,
    target_user_id: int,
    role: str,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(404, "Model not found")

    try:
        crud.require_model_role(
            db,
            user=user,
            model=model,
            min_role="owner",
        )
    except PermissionError:
        raise HTTPException(403, "Owner or admin required")

    perm = crud.add_model_collaborator(
        db,
        model_id=model_id,
        user_id=target_user_id,
        role=role,
    )

    audit.log_event(
        db,
        user_id=user.id,
        action="model.collaborator.add",
        resource_type="model",
        resource_id=model_id,
        extra={
            "target_user_id": target_user_id,
            "role": role,
        },
    )

    return perm


# =========================
# REMOVE COLLABORATOR (AUDITED)
# =========================

@router.delete("/{model_id}/collaborators/{target_user_id}")
def remove_collaborator(
    model_id: int,
    target_user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(404, "Model not found")

    try:
        crud.require_model_role(
            db,
            user=user,
            model=model,
            min_role="owner",
        )
    except PermissionError:
        raise HTTPException(403, "Owner or admin required")

    crud.remove_model_collaborator(
        db,
        model_id=model_id,
        user_id=target_user_id,
    )

    audit.log_event(
        db,
        user_id=user.id,
        action="model.collaborator.remove",
        resource_type="model",
        resource_id=model_id,
        extra={
            "target_user_id": target_user_id,
        },
    )

    return {"status": "removed"}

