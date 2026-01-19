from app.worker.automation_worker import run_worker_once

def test_worker_failure_is_audited(
    db,
    failing_job_db,
    get_latest_job_execution_log,  # 👈 ADD THIS
):
    run_worker_once(db=db)

    log = get_latest_job_execution_log(failing_job_db.id)
    assert log["status"] == "failed"

