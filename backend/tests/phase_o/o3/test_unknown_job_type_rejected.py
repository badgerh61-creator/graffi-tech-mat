from app.services.automation_job_executor import execute_job
from app.services.automation_job_audit import get_latest_job_log

def test_unknown_job_type_rejected(
    db,
    unknown_job,
):
    result = execute_job(db=db, job=unknown_job)

    assert result["status"] == "failed"
    assert "unknown job type" in result["error"]

