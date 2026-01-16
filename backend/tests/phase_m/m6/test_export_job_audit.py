def test_export_job_is_auditable(export_job):
    assert export_job.export_request_id is not None
    assert export_job.created_at is not None

