from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.s3 import get_s3_client
from app.core.config import settings
import uuid

router = APIRouter(prefix="/presign", tags=["presign"])

class PresignRequest(BaseModel):
    filename: str
    content_type: str = "application/octet-stream"

@router.post("/upload")
def presign_upload(req: PresignRequest):
    key = f"uploads/{uuid.uuid4()}/{req.filename}"
    client = get_s3_client()

    if client is None:
        raise HTTPException(500, "S3 client not configured")

    presigned = client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
            "ContentType": req.content_type,
        },
        ExpiresIn=3600,
    )

    public_url = f"{settings.S3_ENDPOINT.rstrip('/')}/{settings.S3_BUCKET}/{key}"

    return {
        "url": presigned,
        "key": key,
        "public_url": public_url
    }
