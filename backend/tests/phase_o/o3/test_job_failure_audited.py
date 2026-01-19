from app.services.automation_job_executor import execute_job
from app.services.automation_job_audit import get_latest_job_log

def test_job_failure_is_audited(
    db,
    failing_job,
):
    execute_job(db=db, job=failing_job)

    record = get_latest_job_log(job_id=failing_job.id)
    assert record["status"] == "failed"

