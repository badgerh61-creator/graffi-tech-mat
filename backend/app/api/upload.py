from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid, io
from ..db.session import get_db
from ..services import s3
from .. import crud, schemas
from ..worker.tasks import process_asset_task

router = APIRouter()

@router.post('/', response_model=schemas.AssetRead)
async def upload_asset(file: UploadFile = File(...), model_id: int | None = None, db: Session = Depends(get_db)):
    key = f'uploads/{uuid.uuid4().hex}_{file.filename}'
    try:
        contents = await file.read()
        s3.upload_fileobj(io.BytesIO(contents), key, content_type=file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'upload failed: {e}')

    asset_in = schemas.AssetCreate(filename=file.filename, content_type=file.content_type, size=len(contents), s3_key=key)
    asset = crud.create_asset(db, asset_in, model_id=model_id)

    process_asset_task.delay(asset.id)
    return asset
