def test_job_can_be_cancelled(export_job):
    export_job.cancel()
    assert export_job.status == "cancelled"

