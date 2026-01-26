# backend/app/services/job_stability.py

from app.models.job import Job

def enforce_job_retry_limit(job):
    """
    Phase S — Job Stability
    Enforces retry exhaustion rule.
    """
    if job.retry_count >= job.max_retries:
        job.status = "failed"


def process_job(db, job):
    if job.retry_count >= job.max_retries:
        job.status = "failed"
        return

    try:
        job.execute()
    except Exception:
        job.retry_count += 1

