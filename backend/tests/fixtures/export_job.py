# tests/fixtures/export_job.py

import pytest
from app.models.export_job import ExportJob

@pytest.fixture
def export_job(db, project, export_request):
    """
    Phase M canonical export job.
    """
    job = ExportJob(
        project_id=project.id,
        export_request_id=export_request.id,  # ✅ INTEGER → INTEGER
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

