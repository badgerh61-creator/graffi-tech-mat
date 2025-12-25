from celery import Celery
import os
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.asset import Asset, AssetStatus
from app.crud import transition_asset_status
from app.services import audit

broker = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

cel = Celery("graffi", broker=broker)


def _get_db() -> Session:
    return SessionLocal()


@cel.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def process_asset_task(self, asset_id: int):
    """
    Canonical asset processing task.

    Guarantees:
    - Idempotent
    - Retry-safe
    - Enforces legal state transitions
    - Audits failures
    """

    db = _get_db()

    try:
        asset = db.query(Asset).get(asset_id)

        # Asset deleted or invalid → nothing to do
        if not asset:
            return {"status": "missing", "asset_id": asset_id}

        # Idempotency: already finished
        if asset.status in (AssetStatus.ready, AssetStatus.failed):
            return {
                "status": "noop",
                "asset_id": asset_id,
                "asset_status": asset.status,
            }

        # created → uploading (only if still created)
        if asset.status == AssetStatus.created:
            transition_asset_status(
                db,
                asset=asset,
                new_status=AssetStatus.uploading,
            )

        # uploading → uploaded
        if asset.status == AssetStatus.uploading:
            transition_asset_status(
                db,
                asset=asset,
                new_status=AssetStatus.uploaded,
            )

        # uploaded → processing
        if asset.status == AssetStatus.uploaded:
            transition_asset_status(
                db,
                asset=asset,
                new_status=AssetStatus.processing,
            )

        # ===== REAL PROCESSING WOULD HAPPEN HERE =====
        # thumbnail generation
        # metadata extraction
        # validation
        # =================================================

        # processing → ready
        transition_asset_status(
            db,
            asset=asset,
            new_status=AssetStatus.ready,
        )

        audit.log_event(
            db,
            user_id=None,
            action="asset.processed",
            resource_type="asset",
            resource_id=asset.id,
        )

        return {
            "status": "ready",
            "asset_id": asset.id,
        }

    except Exception as exc:
        # Hard failure → mark asset failed
        try:
            asset = db.query(Asset).get(asset_id)
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

        raise  # triggers Celery retry
    finally:
        db.close()

