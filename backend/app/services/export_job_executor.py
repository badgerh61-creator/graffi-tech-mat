# backend/app/services/export_job_executor.py

from app.services.image_exporter import _create_image_export_job


def execute_export_job(*, db, job, snapshot, options):
    """
    Phase M.2 canonical execution entrypoint.

    Rules:
    - Job lifecycle is owned here
    - Executor is a thin delegator
    """

    return _create_image_export_job(
        db=db,
        job=job,
        snapshot=snapshot,
        user=None,
        options=options,
    )

