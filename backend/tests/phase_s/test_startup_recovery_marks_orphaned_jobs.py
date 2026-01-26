import pytest

from app.services.startup_recovery import run_startup_recovery

def test_startup_recovery_marks_orphaned_jobs(
    db,
    orphaned_job,
):
    run_startup_recovery(db)

    assert orphaned_job.state == "FAILED"


