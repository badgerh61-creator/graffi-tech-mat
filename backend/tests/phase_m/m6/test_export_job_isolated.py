def test_job_failure_does_not_mutate_snapshot(
    db,
    export_job,
    completed_snapshot,
):
    export_job.mark_failed("render error")

    db.refresh(completed_snapshot)
    assert completed_snapshot.status == "completed"

