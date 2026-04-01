# backend/app/api/upload.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import uuid
import io

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services import storage as s3
from app import crud
from app.models.asset import AssetStatus
from app.schemas import AssetCreate

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_EXTENSIONS = (".glb", ".gltf", ".png", ".jpg", ".hdr")
MAX_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/")
async def upload_asset(
    model_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # ---------------------------------------------------------
    # 🔒 Validate file
    # ---------------------------------------------------------
    if not file.filename or not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(400, "Unsupported file type")

    contents = await file.read()

    if len(contents) > MAX_SIZE:
        raise HTTPException(400, "File too large")

    # ---------------------------------------------------------
    # 🔐 Ensure user can edit this model
    # ---------------------------------------------------------
    model = crud.get_model_if_accessible(
        db,
        model_id=model_id,
        user_id=user.id,
    )

    if not model:
        raise HTTPException(403, "No access to model")

    crud.require_model_role(
        db,
        user=user,
        model=model,
        min_role="editor",
    )

    # ---------------------------------------------------------
    # ☁️ Storage key
    # ---------------------------------------------------------
    key = f"uploads/{uuid.uuid4().hex}_{file.filename}"

    # ---------------------------------------------------------
    # 1️⃣ Create asset row (FIXED — uses schema)
    # ---------------------------------------------------------
    asset = crud.create_asset(
        db=db,
        asset_in=AssetCreate(
            filename=file.filename,
            s3_key=key,
            content_type=file.content_type or "application/octet-stream",
        ),
        model_id=model.id,
        user_id=user.id,
    )

    try:
        # ---------------------------------------------------------
        # 2️⃣ Transition → uploading
        # ---------------------------------------------------------
        crud.transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.uploading,
        )

        # ---------------------------------------------------------
        # 3️⃣ Upload to storage
        # ---------------------------------------------------------
        s3.upload_fileobj(
            io.BytesIO(contents),
            key,
            content_type=file.content_type,
        )

        # ---------------------------------------------------------
        # 4️⃣ Transition → ready
        # ---------------------------------------------------------
        crud.transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.ready,
        )

    except Exception as exc:
        # ---------------------------------------------------------
        # ❌ Failure handling
        # ---------------------------------------------------------
        crud.transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.failed,
            error=str(exc),
        )

        raise HTTPException(503, "Upload failed")

    # ---------------------------------------------------------
    # ✅ Response
    # ---------------------------------------------------------
    return {
        "asset_id": asset.id,
        "model_id": model.id,
        "filename": asset.filename,
        "status": asset.status,
    }
