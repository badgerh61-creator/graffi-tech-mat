# backend/app/services/export_jobs.py

from app.models.export_job import ExportJob


def create_export_job(*, db, export_request=None, project_id=None):
    """
    Phase M job factory.

    - Phase M.1: export_request provided
    - Phase M.2+: job-only execution allowed
    """

    job = ExportJob(
        export_request_id=export_request.id if export_request else None,
        project_id=project_id,
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    return job

