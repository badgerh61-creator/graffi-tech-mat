from app.services.automation_job_executor import execute_job
from app.services.automation_job_audit import get_latest_job_log

def test_job_is_idempotent(
    db,
    automation_job,
):
    result1 = execute_job(db=db, job=automation_job)
    result2 = execute_job(db=db, job=automation_job)

    assert result1["status"] == "succeeded"
    assert result2["status"] == "succeeded"

