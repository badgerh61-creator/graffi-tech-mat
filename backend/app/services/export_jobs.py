# app/services/export_jobs.py

from app.models.export_job import ExportJob

def create_export_job(db, export_request_id):
    job = ExportJob(
        export_request_id=str(export_request_id)
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

