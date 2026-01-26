from app.services.job_stability import enforce_job_retry_limit

def test_job_retry_exhaustion_marks_failed(db, failing_job):
    enforce_job_retry_limit(failing_job)
    db.commit()

    assert failing_job.status == "failed"


