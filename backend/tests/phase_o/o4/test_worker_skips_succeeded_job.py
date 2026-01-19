from app.worker.automation_worker import run_worker_once

def test_worker_skips_succeeded_job(
    db,
    succeeded_job,
):
    run_worker_once(db=db)

    assert succeeded_job.attempt == 0

