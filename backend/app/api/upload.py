from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid, io

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services import storage as s3
from app import crud, schemas
from app.worker.tasks import process_asset_task

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

    s3.upload_fileobj(
        io.BytesIO(contents),
        key,
        content_type=file.content_type,
    )

    model = None
    if file.filename.lower().endswith(".glb"):
        model = crud.create_model(
            db,
            schemas.ModelCreate(name=file.filename),
            owner_id=user.id,
        )

    asset = crud.create_asset(
        db,
        schemas.AssetCreate(
            filename=file.filename,
            content_type=file.content_type,
            size=len(contents),
            s3_key=key,
        ),
        model_id=model.id if model else None,
    )

    process_asset_task.delay(asset.id)
    return asset

