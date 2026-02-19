from datetime import datetime

def test_job_final_failure_after_max_attempts(db, job_factory):
    from app.services.job_reliability import run_job_once, RetryPolicy

    now = datetime(2026, 1, 20, 12, 0, 0)
    job = job_factory(status="QUEUED", attempts=2, max_attempts=3, next_run_at=now)

    def handler(_job):
        raise RuntimeError("boom")

    updated = run_job_once(
        db=db,
        job=job,
        now=now,
        handler=handler,
        policy=RetryPolicy(max_attempts=3, base_backoff_seconds=5, stuck_job_seconds=60),
    )

    assert updated.attempts == 3
    assert updated.status == "FAILED"

