import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import AssetCreate
from app import crud
from app.services import s3
from app.worker import tasks

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/asset")
async def upload_asset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    asset_id = str(uuid.uuid4())
    filename = file.filename
    extension = filename.split(".")[-1].lower()
    mime = file.content_type or "application/octet-stream"

    # Read file bytes
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Build S3 key
    s3_key = f"uploads/{asset_id}/{filename}"

    # Upload to S3/MinIO
    url = s3.upload_bytes(s3_key, data, content_type=mime)

    # Determine asset type
    if mime.startswith("image/"):
        asset_type = "image"
    elif extension in ["glb", "gltf", "fbx", "obj", "usdz"]:
        asset_type = "model"
    elif extension in ["hdr", "exr"]:
        asset_type = "hdri"
    else:
        asset_type = "file"

    # Thumbnail (images only)
    thumbnail_url = None
    if asset_type == "image":
        tasks.enqueue_create_thumbnail(asset_id, filename, data)

    # Build asset object
    asset_data = AssetCreate(
        id=asset_id,
        name=filename,
        type=asset_type,
        url=url,
        thumbnail_url=thumbnail_url,
        size=len(data),
        meta={
            "ext": extension,
            "mime": mime,
            "s3_key": s3_key,
        },
    )

    # Save in DB
    db_asset = crud.create_asset(db, asset_data)

    return {
        "ok": True,
        "asset": db_asset.id,
        "url": db_asset.url,
    }
