# app/services/export_requests.py

from app.services.export_jobs import create_export_job

def on_export_request_accepted(db, export_request_id):
    """
    Called after an export request is validated and accepted.

    Side effects:
    - Creates exactly one ExportJob
    - Does NOT mutate snapshots
    - Does NOT execute the job
    """
    return create_export_job(
        db,
        str(export_request_id),
    )

