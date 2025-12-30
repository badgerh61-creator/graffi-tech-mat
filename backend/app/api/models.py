# =========================================
# Graffi-Tech-Mat — Models API
# Phase 4.6 — STEP 3 FINAL (STABLE)
# =========================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_viewer, require_editor
from app import crud
from app.services import storage as s3
from app.services import audit
from app.services.email import send_invite_email

from app.schemas import ModelCreate, ModelRead
from app.models.asset import AssetStatus
from app.models.model_permission import ModelPermission

router = APIRouter(prefix="/models", tags=["models"])

MODEL_URL_EXPIRES = 300


# =====================================================
# LIST MODELS — ROLE AWARE
# =====================================================

@router.get("/", response_model=list[ModelRead])
def list_models(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    rows = crud.get_models_accessible_to_user(db, user.id)
    results = []

    for model, role in rows:
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


# =====================================================
# CREATE MODEL — EDITOR / ADMIN
# =====================================================

@router.post("/", response_model=ModelRead)
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
        extra={"name": model.name},
    )

    return ModelRead(
        id=model.id,
        name=model.name,
        description=model.description,
        owner_id=model.owner_id,
        created_at=model.created_at,
        role="owner",
        assets=model.assets,
    )


# =====================================================
# GET MODEL GLB URL — VIEWER+
# =====================================================

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
        if asset.filename.lower().endswith(".glb") and asset.status == AssetStatus.ready:
            return {
                "url": s3.get_presigned_url(asset.s3_key, MODEL_URL_EXPIRES),
                "expires_in": MODEL_URL_EXPIRES,
                "asset_id": asset.id,
            }

    raise HTTPException(404, "No ready GLB asset attached")


# =====================================================
# INVITE USER — OWNER ONLY
# =====================================================

@router.post("/{model_id}/invites")
def invite_by_email(
    model_id: int,
    email: str,
    role: str = "viewer",
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    model = crud.get_model_by_id(db, model_id)
    if not model:
        raise HTTPException(404, "Model not found")

    try:
        crud.require_owner(db, user=user, model=model)
    except PermissionError:
        raise HTTPException(403, "Owner access required")

    existing_user = crud.get_user_by_email(db, email)
    if existing_user:
        perm = ModelPermission(
            model_id=model.id,
            user_id=existing_user.id,
            role=role,
        )
        db.add(perm)
        db.commit()
        return {"status": "accepted"}

    invite = crud.create_model_invite(
        db,
        model=model,
        email=email,
        role=role,
    )

    send_invite_email(
        to_email=email,
        model_name=model.name,
        role=role,
        token=invite.token,
    )

    audit.log_event(
        db,
        user_id=user.id,
        action="model.invite.sent",
        resource_type="model",
        resource_id=model.id,
        extra={"email": email, "role": role},
    )

    return {"status": "sent"}


# =====================================================
# ACCEPT INVITE
# =====================================================

@router.post("/invites/{token}/accept")
def accept_invite(
    token: str,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    invite = crud.get_invite_by_token(db, token)
    if not invite:
        raise HTTPException(404, "Invalid invite")

    if invite.email.lower() != user.email.lower():
        raise HTTPException(403, "Invite email mismatch")

    crud.accept_model_invite(db, invite=invite, user=user)

    audit.log_event(
        db,
        user_id=user.id,
        action="model.invite.accepted",
        resource_type="model",
        resource_id=invite.model_id,
    )

    return {"status": "accepted"}

