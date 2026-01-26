from app.models.job import Job


def run_startup_recovery(db):
    """
    Phase S — Startup Recovery

    On system startup:
    - Any RUNNING job is considered orphaned
    - Orphaned jobs are marked FAILED
    """

    orphaned_jobs = (
        db.query(Job)
        .filter(Job.state == "RUNNING")
        .all()
    )

    for job in orphaned_jobs:
        job.state = "FAILED"

    db.commit()

    return orphaned_jobs

