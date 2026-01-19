from app.worker.automation_worker import run_worker_once

def test_worker_executes_pending_job(
    db,
    pending_job,
):
    run_worker_once(db=db)

    assert pending_job.status in ("succeeded", "failed")

