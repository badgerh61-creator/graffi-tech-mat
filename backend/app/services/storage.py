from minio import Minio
from app.core.config import settings
from fastapi import UploadFile
from datetime import timedelta
import io

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)


def ensure_bucket():
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)


# ===========================
# Upload via UploadFile
# ===========================
def upload_file(*, file: UploadFile, object_name: str):
    ensure_bucket()
    client.put_object(
        settings.MINIO_BUCKET,
        object_name,
        file.file,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=file.content_type,
    )


# ===========================
# Upload via BytesIO
# ===========================
def upload_fileobj(
    fileobj: io.BytesIO,
    object_name: str,
    content_type: str | None = None,
):
    ensure_bucket()
    client.put_object(
        settings.MINIO_BUCKET,
        object_name,
        fileobj,
        length=fileobj.getbuffer().nbytes,
        content_type=content_type or "application/octet-stream",
    )


# ===========================
# Presigned URLs (EXPIRABLE)
# ===========================
def get_presigned_url(
    object_name: str,
    expires_seconds: int = 3600,
) -> str:
    ensure_bucket()
    return client.presigned_get_object(
        settings.MINIO_BUCKET,
        object_name,
        expires=timedelta(seconds=expires_seconds),
    )

