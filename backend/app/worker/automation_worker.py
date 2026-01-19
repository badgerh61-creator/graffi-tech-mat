from app.models.automation_job import AutomationJob
from app.services.automation_job_executor import execute_job


def run_worker_once(*, db):
    """
    Execute a single pending automation job.

    Responsibilities:
    - select the next pending job
    - invoke execution
    - persist state changes

    This worker does NOT:
    - implement retry logic
    - emit audit records
    - decide job outcomes
    """

    job = (
        db.query(AutomationJob)
        .filter(AutomationJob.status == "pending")
        .order_by(AutomationJob.created_at.asc())
        .first()
    )

    if not job:
        return None

    result = execute_job(db=db, job=job)

    # 🔒 Persistence is the worker’s responsibility
    db.commit()

    return result

