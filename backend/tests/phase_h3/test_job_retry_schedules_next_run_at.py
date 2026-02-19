from datetime import datetime

def test_job_retry_schedules_next_run_at(db, job_factory):
    from app.services.job_reliability import run_job_once, RetryPolicy

    now = datetime(2026, 1, 20, 12, 0, 0)
    job = job_factory(status="QUEUED", attempts=0, max_attempts=3, next_run_at=now)

    def handler(_job):
        raise RuntimeError("boom")

    policy = RetryPolicy(max_attempts=3, base_backoff_seconds=5, stuck_job_seconds=60)
    updated = run_job_once(db=db, job=job, now=now, handler=handler, policy=policy)

    assert updated.status == "QUEUED"
    assert updated.attempts == 1
    assert updated.next_run_at is not None
    assert updated.next_run_at > now

