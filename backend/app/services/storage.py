from minio import Minio, S3Error
from app.core.config import settings
from datetime import timedelta
import io
import time
import logging

log = logging.getLogger(__name__)

# --------------------------------------------------
# LAZY CLIENT (CRITICAL FIX)
# --------------------------------------------------

_client: Minio | None = None
_BUCKET_READY = False


def get_client() -> Minio:
    """
    Lazily initialize MinIO client.
    NEVER create network clients at import time.
    """
    global _client

    if _client is None:
        if not settings.MINIO_ENDPOINT:
            raise RuntimeError("MINIO_ENDPOINT is not configured")

        _client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

    return _client


def ensure_bucket():
    global _BUCKET_READY
    if _BUCKET_READY:
        return

    client = get_client()

    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)

    _BUCKET_READY = True


# --------------------------------------------------
# RETRY WRAPPER
# --------------------------------------------------

def _retry(op, attempts=3, backoff=0.5):
    last = None
    for i in range(attempts):
        try:
            return op()
        except S3Error as exc:
            last = exc
            log.warning(
                "MinIO retry %s/%s failed: %s",
                i + 1,
                attempts,
                exc,
            )
            time.sleep(backoff * (2 ** i))
    raise last


# --------------------------------------------------
# PUBLIC API
# --------------------------------------------------

def upload_fileobj(
    fileobj: io.BytesIO,
    key: str,
    *,
    content_type: str | None = None,
):
    ensure_bucket()
    size = fileobj.getbuffer().nbytes
    client = get_client()

    def _op():
        client.put_object(
            settings.MINIO_BUCKET,
            key,
            fileobj,
            length=size,
            content_type=content_type or "application/octet-stream",
        )

    return _retry(_op)


def get_presigned_url(
    key: str,
    expires_seconds: int = 3600,
) -> str:
    ensure_bucket()
    client = get_client()

    return client.presigned_get_object(
        settings.MINIO_BUCKET,
        key,
        expires=timedelta(seconds=expires_seconds),
    )

