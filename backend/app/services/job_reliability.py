from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services import audit
from app.services.metrics import emit_metric
from app.models.job import Job


# Canonical states (match your existing "CREATED" style)
JOB_QUEUED = "QUEUED"
JOB_RUNNING = "RUNNING"
JOB_SUCCEEDED = "SUCCEEDED"
JOB_FAILED = "FAILED"


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 5
    base_backoff_seconds: int = 5
    stuck_job_seconds: int = 60


def compute_backoff_seconds(*, attempts: int, base: int) -> int:
    return min(base * (2 ** max(0, attempts - 1)), 300)


def schedule_retry(*, job: Job, now: datetime, policy: RetryPolicy) -> None:
    backoff = compute_backoff_seconds(attempts=job.attempts, base=policy.base_backoff_seconds)
    job.next_run_at = now + timedelta(seconds=backoff)
    job.status = JOB_QUEUED
    emit_metric("job.retry_scheduled", 1, tags={"job_type": job.job_type})


def mark_final_failed(*, db: Session, job: Job, user_id: Optional[int] = None) -> None:
    job.status = JOB_FAILED
    emit_metric("job.failed_final", 1, tags={"job_type": job.job_type})
    audit.log_event(
        db,
        user_id=user_id,
        action="job.failed_final",
        resource_type="job",
        resource_id=job.id,
        extra={"attempts": job.attempts, "max_attempts": job.max_attempts},
    )


def recover_stuck_jobs(*, db: Session, now: datetime, policy: RetryPolicy) -> int:
    cutoff = now - timedelta(seconds=policy.stuck_job_seconds)

    stuck = (
        db.query(Job)
        .filter(Job.state == JOB_RUNNING)  # use underlying column for query stability
        .filter(Job.started_at < cutoff)
        .all()
    )

    recovered = 0
    for job in stuck:
        if job.attempts < job.max_attempts:
            job.status = JOB_QUEUED
            job.next_run_at = now
            recovered += 1
            emit_metric("job.recovered_stuck", 1, tags={"job_type": job.job_type})
            audit.log_event(
                db,
                user_id=None,
                action="job.recovered_stuck",
                resource_type="job",
                resource_id=job.id,
                extra={"attempts": job.attempts, "max_attempts": job.max_attempts},
            )
        else:
            mark_final_failed(db=db, job=job, user_id=None)

    db.commit()
    return recovered


def run_job_once(
    *,
    db: Session,
    job: Job,
    now: datetime,
    handler: Callable[[Job], None],
    policy: RetryPolicy,
) -> Job:
    if job.status not in (JOB_QUEUED, JOB_RUNNING):
        raise HTTPException(409, "Job not runnable")

    if job.next_run_at and now < job.next_run_at:
        return job

    job.status = JOB_RUNNING
    job.started_at = now
    db.commit()

    try:
        handler(job)
        job.status = JOB_SUCCEEDED
        job.finished_at = now
        db.commit()
        return job
    except Exception as e:
        job.attempts = int(job.attempts or 0) + 1
        job.last_error = str(e)

        if job.attempts >= job.max_attempts:
            mark_final_failed(db=db, job=job, user_id=None)
        else:
            schedule_retry(job=job, now=now, policy=policy)

        db.commit()
        return job

