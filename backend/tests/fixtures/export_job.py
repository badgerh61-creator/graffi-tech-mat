# tests/fixtures/export_job.py

import pytest
import uuid
from app.models.export_job import ExportJob


@pytest.fixture
def export_job(db, project):
    """
    Phase M canonical export job fixture.

    Represents a freshly created job:
    - status = requested
    - no execution performed
    - lifecycle transitions are test-controlled
    """
    job = ExportJob(
        export_request_id=str(uuid.uuid4()),
        project_id=project.id,
        # ❗ DO NOT set status — default must apply
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

