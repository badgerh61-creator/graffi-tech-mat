from sqlalchemy.orm import Session
from datetime import datetime

from app.models.job import Job
from app.models.asset import Asset
from app.services.thumbnails import generate_thumbnail_for_asset


class JobExecutor:
    """
    Phase I.6 — Manual Job Execution (SAFE)

    - Explicit state transitions
    - No async
    - No retries
    - No background workers
    """

    @staticmethod
    def execute(*, db: Session, job: Job) -> None:
        if job.state != "CREATED":
            raise RuntimeError(f"Job {job.id} is not executable")

        # ---- RUNNING ----
        job.state = "RUNNING"
        job.updated_at = datetime.utcnow()
        db.add(job)
        db.flush()

        try:
            if job.job_type == "THUMBNAIL_GENERATION":
                asset = db.query(Asset).filter(
                    Asset.id == job.target_id
                ).first()

                if not asset:
                    raise RuntimeError(
                        f"Asset {job.target_id} not found"
                    )

                generate_thumbnail_for_asset(
                    db=db,
                    asset=asset,
                )

            else:
                raise RuntimeError(
                    f"Unknown job type: {job.job_type}"
                )

            # ---- COMPLETED ----
            job.state = "COMPLETED"
            job.updated_at = datetime.utcnow()
            db.add(job)

        except Exception:
            job.state = "FAILED"
            job.updated_at = datetime.utcnow()
            db.add(job)
            raise

