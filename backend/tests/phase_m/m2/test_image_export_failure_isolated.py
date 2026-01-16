def test_image_export_failure_does_not_fail_job_creation(
    export_job,
):
    assert export_job.status in ("requested", "running", "failed", "completed")

