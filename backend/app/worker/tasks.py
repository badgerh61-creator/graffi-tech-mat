# app/worker/tasks.py
import io
from PIL import Image
from rq import Queue
from redis import Redis
from app.services.s3 import get_s3_client, upload_bytes, build_public_url
from app.core.config import settings
from app.db.session import SessionLocal
from app.db import models as db_models

# create redis connection using REDIS_URL env var
def _redis_conn():
    import os
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    return Redis.from_url(url)

def enqueue_create_thumbnail_by_key(asset_id: str, s3_key: str, filename: str):
    q = Queue(connection=_redis_conn())
    q.enqueue(process_thumbnail_by_key, asset_id, s3_key, filename)

def process_thumbnail_by_key(asset_id: str, s3_key: str, filename: str):
    """
    Worker job: fetch bytes from S3 (stream), create webp thumbnail, upload, update DB.
    """
    # get the bytes from S3
    s3 = get_s3_client()
    try:
        resp = s3.get_object(Bucket=settings.S3_BUCKET, Key=s3_key)
        body = resp["Body"].read()
    except Exception as e:
        # log or requeue as you prefer
        return {"error": f"failed to download from s3: {e}"}

    # create thumbnail bytes
    thumb_bytes = _create_thumbnail_bytes(body)

    thumb_key = f"thumbs/{asset_id}/{filename}.webp"
    try:
        thumb_url = upload_bytes(thumb_key, thumb_bytes, content_type="image/webp")
    except Exception as e:
        return {"error": f"failed to upload thumb: {e}"}

    # update DB (SessionLocal from your codebase)
    db = SessionLocal()
    try:
        a = db.query(db_models.Asset).filter(db_models.Asset.id == asset_id).first()
        if a:
            a.thumbnail_url = thumb_url
            # optionally set size if missing
            if not a.size:
                a.size = len(body)
            db.commit()
    finally:
        db.close()

    return {"thumb_url": thumb_url}

def _create_thumbnail_bytes(data: bytes, size=(512, 512)):
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    im.thumbnail(size, Image.LANCZOS)
    bg = Image.new("RGBA", size, (255, 255, 255, 0))
    x = (size[0] - im.width) // 2
    y = (size[1] - im.height) // 2
    bg.paste(im, (x, y), im)
    out = io.BytesIO()
    bg.save(out, format="WEBP", quality=80)
    out.seek(0)
    return out.read()
