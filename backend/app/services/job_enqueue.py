from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.job import Job


def enqueue_job(
    *,
    db: Session,
    name: str,
    payload: dict,
    idempotency_key: str,
    max_attempts: int = 5,
    mutation_id: int = 1,
    target_type: str = "system",
    target_id: int = 1,
) -> Job:
    """
    H.3 enqueue, adapted to your Job schema.

    - name -> job_type (your schema)
    - payload is accepted for interface compatibility but not stored in Job (schema has no payload column)
    - status/state uses your canonical 'state' field via .status property
    """

    existing = db.query(Job).filter(Job.idempotency_key == idempotency_key).first()
    if existing:
        return existing

    job = Job(
        mutation_id=mutation_id,
        job_type=name,
        target_type=target_type,
        target_id=target_id,
        idempotency_key=idempotency_key,
        max_retries=max_attempts,     # maps via compatibility property max_attempts too
        retry_count=0,                # maps via attempts too
        next_run_at=datetime.utcnow(),
    )

    # Canonical lifecycle (use your canonical strings)
    job.status = "QUEUED"

    db.add(job)
    db.commit()
    db.refresh(job)
    return job

