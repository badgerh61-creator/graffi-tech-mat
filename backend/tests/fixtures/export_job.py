# tests/fixtures/export_job.py

import pytest
import uuid
from app.models.export_job import ExportJob

@pytest.fixture
def export_job(db, project):
    job = ExportJob(
        export_request_id=str(uuid.uuid4()),
        project_id=project.id,
        status="completed",
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

