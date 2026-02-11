# backend/app/worker/tasks.py

from celery import Celery
import os
import io
import tempfile
from sqlalchemy.orm import Session

import trimesh
import numpy as np
from PIL import Image

from app.db.session import SessionLocal
from app.models.asset import Asset, AssetStatus
from app.services import audit, storage as s3

broker = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

cel = Celery("graffi", broker=broker)


def _get_db() -> Session:
    return SessionLocal()


@cel.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def process_asset_task(self, asset_id: int):
    """
    Phase 11.1 — REAL asset processing

    Guarantees:
    - Idempotent
    - Retry-safe
    - Preserves Phase-10 transitions
    """

    # 🔑 LOCAL IMPORT (breaks circular dependency)
    from app.crud import transition_asset_status

    db = _get_db()

    try:
        asset = db.get(Asset, asset_id)

        if not asset:
            return {"status": "missing", "asset_id": asset_id}

        if asset.status in (AssetStatus.ready, AssetStatus.failed):
            return {"status": "noop", "asset_id": asset.id}

        if asset.status == AssetStatus.created:
            transition_asset_status(db, asset=asset, new_status=AssetStatus.uploading)

        if asset.status == AssetStatus.uploading:
            transition_asset_status(db, asset=asset, new_status=AssetStatus.uploaded)

        if asset.status == AssetStatus.uploaded:
            transition_asset_status(db, asset=asset, new_status=AssetStatus.processing)

        # ================= REAL PROCESSING =================

        # Download GLB from storage
        with tempfile.NamedTemporaryFile(suffix=".glb") as tmp:
            obj = s3.client.get_object(
                s3.settings.MINIO_BUCKET,
                asset.s3_key,
            )
            data = obj.read()
            tmp.write(data)
            tmp.flush()

            mesh = trimesh.load(tmp.name, force="mesh")

        # Metadata extraction
        metadata = {
            "vertex_count": int(len(mesh.vertices)),
            "faces": int(len(mesh.faces)),
            "bounds": mesh.bounds.tolist(),
            "format": "glb",
            "file_size": asset.size,
        }

        asset.asset_metadata = metadata
        db.commit()

        audit.log_event(
            db,
            user_id=None,
            action="asset.metadata.extracted",
            resource_type="asset",
            resource_id=asset.id,
        )

        # Thumbnail generation
        scene = mesh.scene()
        png = scene.save_image(resolution=(512, 512))

        thumb_key = f"thumbnails/{asset.id}.png"
        s3.upload_fileobj(
            io.BytesIO(png),
            thumb_key,
            content_type="image/png",
        )

        asset.thumbnail_key = thumb_key
        db.commit()

        audit.log_event(
            db,
            user_id=None,
            action="asset.thumbnail.generated",
            resource_type="asset",
            resource_id=asset.id,
        )

        # processing → ready
        transition_asset_status(db, asset=asset, new_status=AssetStatus.ready)

        audit.log_event(
            db,
            user_id=None,
            action="asset.processed",
            resource_type="asset",
            resource_id=asset.id,
        )

        return {"status": "ready", "asset_id": asset.id}

    except Exception as exc:
        try:
            asset = db.get(Asset, asset_id)
            if asset and asset.status not in (AssetStatus.ready, AssetStatus.failed):
                transition_asset_status(
                    db,
                    asset=asset,
                    new_status=AssetStatus.failed,
                    error=str(exc),
                )

                audit.log_event(
                    db,
                    user_id=None,
                    action="asset.failed",
                    resource_type="asset",
                    resource_id=asset.id,
                    extra={"error": str(exc)},
                )
        finally:
            db.close()

        raise

    finally:
        db.close()

