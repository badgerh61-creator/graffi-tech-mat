from app.services.automation_job_executor import execute_job

def test_automation_job_metrics_emitted(
    metrics_collector,
    automation_job,
    db,
):
    execute_job(db=db, job=automation_job)

    assert metrics_collector.count("automation.job.run.count") == 1

