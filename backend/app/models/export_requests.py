from app.services.export_jobs import create_export_job

def on_export_request_accepted(db, export_request_id):
    create_export_job(db, export_request_id)

