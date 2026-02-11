# backend/app/services/image_exporter.py

from app.models.export_job import ExportJob
from app.models.export_artifact import ExportArtifact
from app.services.image_export import run_image_export
from app.services import audit


def create_image_export_legacy(
    *,
    db,
    snapshot,
    user,
    format,
    resolution=None,
):
    """
    Phase E compatibility wrapper.
    Converts legacy export calls into Phase M job-based execution.
    """

    from app.services.export_job_executor import execute_export_job

    job = ExportJob(
        project_id=snapshot.project_id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    execute_export_job(
        db=db,
        job=job,
        snapshot=snapshot,
        options={
            "format": format,
            "resolution": resolution,
        },
    )

    return job


def _create_image_export_job(*, db, job: ExportJob, snapshot, user, options):
    """
    Phase M.2 canonical job-based image export.
    """

    if snapshot.status != "completed":
        raise ValueError("Snapshot not exportable")

    job.mark_running()
    db.commit()

    try:
        result = run_image_export(
            snapshot=snapshot,
            options=options,
        )

        artifact = ExportArtifact.completed(
            bytes=result.bytes,
            hash=result.hash,
            format=result.format,
            snapshot_id=snapshot.id,
            export_job_id=job.id,
        )

        db.add(artifact)
        job.mark_completed()
        db.commit()

        audit.log_event(
            db=db,
            user_id=user.id if user else None,
            action="export.image.completed",
            resource_type="export_job",
            resource_id=job.id,
            extra={
                "artifact_id": artifact.id,
                "format": artifact.format,
            },
        )

        return artifact

    except Exception as exc:
        job.mark_failed(reason=str(exc))
        db.commit()
        raise


def create_image_export(*, db, snapshot, user, format, resolution=None):
    """
    Phase E canonical API (INTENT ONLY).

    - Creates an export job
    - Queues it
    - Emits audit event
    - DOES NOT execute
    """

    from app.models.export_job import ExportJob

    if snapshot.status != "completed":
        raise ValueError("Snapshot not exportable")

    job = ExportJob(
        project_id=snapshot.project_id,
        export_request_id=None,  # Phase E has no export_request
        status="queued",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    audit.log_event(
        db=db,
        user_id=user.id,
        action="snapshot.export.image",
        resource_type="export_job",
        resource_id=job.id,
        extra={
            "snapshot_id": snapshot.id,
            "format": format,
        },
    )

    return job

