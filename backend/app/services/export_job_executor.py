from app.services.image_export import run_image_export

def execute_export_job(db, job, export_request, snapshot):
    job.mark_running()

    try:
        artifact = run_image_export(
            db=db,
            snapshot=snapshot,
            options=export_request.options,
        )
        job.mark_completed()
        return artifact
    except Exception:
        job.mark_failed()
        raise

