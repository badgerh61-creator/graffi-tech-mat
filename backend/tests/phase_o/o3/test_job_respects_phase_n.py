from app.services.automation_job_executor import execute_job
from app.services.automation_job_audit import get_latest_job_log

def test_job_cannot_bypass_phase_n(
    db,
    forbidden_job,
):
    result = execute_job(db=db, job=forbidden_job)

    assert result["status"] == "failed"

