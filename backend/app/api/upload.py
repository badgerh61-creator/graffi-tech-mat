from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid, io

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services import storage as s3
from app import crud, schemas
from app.models.asset import AssetStatus

router = APIRouter(prefix="/upload", tags=["upload"])

ALLOWED_EXTENSIONS = (".glb", ".gltf", ".png", ".jpg", ".hdr")
MAX_SIZE = 50 * 1024 * 1024  # 50MB


@router.post("/")
async def upload_asset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(400, "Unsupported file type")

    contents = await file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(400, "File too large")

    key = f"uploads/{uuid.uuid4().hex}_{file.filename}"

    # 1️⃣ Create asset row FIRST
    asset = crud.create_asset(
        db,
        schemas.AssetCreate(
            filename=file.filename,
            content_type=file.content_type,
            size=len(contents),
            s3_key=key,
        ),
    )

    try:
        crud.transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.uploading,
        )

        # 2️⃣ Upload to storage
        s3.upload_fileobj(
            io.BytesIO(contents),
            key,
            content_type=file.content_type,
        )

        crud.transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.uploaded,
        )

    except Exception as exc:
        crud.transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.failed,
            error=str(exc),
        )
        raise HTTPException(503, "Upload failed")

    return asset

