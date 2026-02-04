# backend/app/services/jobs/export_queue.py

from app.models.export_job import ExportJob


def enqueue_export_job(*, db, export_record):
    """
    Phase E stub.
    Registers execution record only.
    NO execution performed here.
    """

    job = ExportJob(
        export_request_id=export_record.id,
        status="requested",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # 🔗 link intent → job
    export_record.job_id = job.id
    db.add(export_record)
    db.commit()

    return job

