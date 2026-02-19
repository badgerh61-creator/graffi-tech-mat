from datetime import datetime, timedelta

def test_recover_stuck_jobs_marks_failed_when_no_attempts_left(db, job_factory):
    from app.services.job_reliability import recover_stuck_jobs, RetryPolicy

    now = datetime(2026, 1, 20, 12, 0, 0)
    started = now - timedelta(seconds=120)

    job = job_factory(
        status="RUNNING",
        attempts=3,
        max_attempts=3,
        started_at=started,
    )

    count = recover_stuck_jobs(db=db, now=now, policy=RetryPolicy(stuck_job_seconds=60))
    assert count == 0

    db.refresh(job)
    assert job.status == "FAILED"

