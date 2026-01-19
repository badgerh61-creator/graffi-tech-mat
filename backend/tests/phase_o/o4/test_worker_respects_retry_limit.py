from app.worker.automation_worker import run_worker_once

def test_worker_respects_retry_limit(
    db,
    failing_job_db,
):
    for _ in range(10):
        run_worker_once(db=db)

    assert failing_job_db.attempt == failing_job_db.max_attempts

