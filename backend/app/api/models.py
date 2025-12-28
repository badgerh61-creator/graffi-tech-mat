from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.deps import require_viewer, require_editor
from app import crud
from app.services import storage as s3
from app.services import audit
from app.services.email import send_invite_email
from app.schemas import ModelCreate
from app.models.asset import AssetStatus
from app.models.model_permission import ModelPermission
from app.models.model_invite import InviteStatus

router = APIRouter(prefix="/models", tags=["models"])

MODEL_URL_EXPIRES = 300
EXPORT_URL_EXPIRES = 300


@router.get("/")
def list_models(
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    return crud.get_models_accessible_to_user(db, user.id)


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
        extra={"name": model.name},
    )

    return model


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
        if (
            asset.filename.lower().endswith(".glb")
            and asset.status == AssetStatus.ready
        ):
            return {
                "url": s3.get_presigned_url(asset.s3_key, MODEL_URL_EXPIRES),
                "expires_in": MODEL_URL_EXPIRES,
                "asset_id": asset.id,
            }

    raise HTTPException(404, "No ready GLB asset attached")


@router.get("/{model_id}/exports/{export_type}")
def export_model(
    model_id: int,
    export_type: str,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    if export_type != "original_glb":
        raise HTTPException(400, "Unsupported export type")

    model = crud.get_model_if_accessible(
        db,
        model_id=model_id,
        user_id=user.id,
    )
    if not model:
        raise HTTPException(404, "Model not found or no access")

    for asset in model.assets:
        if (
            asset.filename.lower().endswith(".glb")
            and asset.status == AssetStatus.ready
        ):
            audit.log_event(
                db,
                user_id=user.id,
                action="model.export.downloaded",
                resource_type="model",
                resource_id=model.id,
                extra={"type": export_type},
            )

            return {
                "url": s3.get_presigned_url(asset.s3_key, EXPORT_URL_EXPIRES),
                "expires_in": EXPORT_URL_EXPIRES,
                "type": export_type,
            }

    raise HTTPException(404, "Export not available")


@router.post("/{model_id}/invites")
def invite_by_email(
    model_id: int,
    email: str,
    role: str = "viewer",
    db: Session = Depends(get_db),
    user=Depends(require_editor),
):
    model = crud.get_model_if_accessible(
        db,
        model_id=model_id,
        user_id=user.id,
    )
    if not model:
        raise HTTPException(404, "Model not found or no access")

    crud.require_owner(db, user=user, model=model)

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
        invited_by_id=user.id,
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

    return invite


@router.post("/invites/{token}/accept")
def accept_invite(
    token: str,
    db: Session = Depends(get_db),
    user=Depends(require_viewer),
):
    invite = crud.get_invite_by_token(db, token)
    if not invite or invite.status != InviteStatus.pending:
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

