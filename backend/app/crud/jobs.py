# backend/app/crud/jobs.py

from sqlalchemy.orm import Session

from app.models.job import Job


def create_job(
    db: Session,
    *,
    mutation_id: int,
    job_type: str,
    target_type: str,
    target_id: int,
) -> Job:
    job = Job(
        mutation_id=mutation_id,
        job_type=job_type,
        target_type=target_type,
        target_id=target_id,
        state="CREATED",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

