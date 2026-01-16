# tests/fixtures/export_job.py

import pytest
import uuid
from app.models.export_job import ExportJob

@pytest.fixture
def export_job(db):
    job = ExportJob(
        export_request_id=str(uuid.uuid4())
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

