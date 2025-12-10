from fastapi import APIRouter, HTTPException
from ..services import s3
from ..schemas import PresignResponse
import uuid

router = APIRouter()

@router.post('/', response_model=PresignResponse)
def presign_upload(filename: str, content_type: str | None = None, expire_seconds: int = 3600):
    if not filename:
        raise HTTPException(status_code=400, detail='filename is required')
    key = f'uploads/{uuid.uuid4().hex}_{filename}'
    try:
        presigned = s3.create_presigned_post(key, expires_in=expire_seconds)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'could not create presign: {e}')

    url = presigned.get('url') or ''
    fields = presigned.get('fields')
    return PresignResponse(url=url, fields=fields, expire_seconds=expire_seconds)
