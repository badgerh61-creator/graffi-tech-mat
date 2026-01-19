from app.services.automation_job_executor import execute_job
from app.services.automation_job_audit import get_latest_job_log

def test_job_retry_limit_enforced(
    db,
    failing_job,
):
    for _ in range(5):
        execute_job(db=db, job=failing_job)

    assert failing_job.attempt == failing_job.max_attempts
    assert failing_job.status == "failed"

