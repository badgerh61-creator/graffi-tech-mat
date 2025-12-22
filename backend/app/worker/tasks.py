# backend/app/worker/tasks.py

from celery import Celery
import os

broker = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

cel = Celery("graffi", broker=broker)


@cel.task
def generate_thumbnail(asset_id):
    """
    Placeholder task for thumbnail generation.
    Safe no-op for now.
    """
    return {
        "asset_id": asset_id,
        "status": "thumbnail_ok",
    }


@cel.task
def process_asset_task(asset_id: int):
    """
    Task expected by upload API.

    This is a SAFE STUB so backend can boot and
    uploads do not crash. Real processing can
    be added later without changing imports.
    """
    # In future:
    # - generate thumbnail
    # - extract metadata
    # - notify client
    return {
        "asset_id": asset_id,
        "status": "processed",
    }

