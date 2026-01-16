def test_job_status_transitions_are_valid(export_job):
    assert export_job.status == "requested"

    export_job.mark_running()
    assert export_job.status == "running"

    export_job.mark_completed()
    assert export_job.status == "completed"

