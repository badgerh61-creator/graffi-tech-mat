import pytest
from app.services.automation_job_audit import get_latest_job_log


@pytest.fixture
def pending_job(db, automation_job):
    db.add(automation_job)
    db.commit()
    return automation_job


@pytest.fixture
def failing_job_db(db, failing_job):
    db.add(failing_job)
    db.commit()
    return failing_job


@pytest.fixture
def succeeded_job(db, automation_job):
    automation_job.status = "succeeded"
    automation_job.attempt = 0
    db.add(automation_job)
    db.commit()
    return automation_job


@pytest.fixture
def get_latest_job_execution_log():
    return get_latest_job_log

