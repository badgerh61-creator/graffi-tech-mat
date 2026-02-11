# backend/app/services/export_requests.py

from fastapi import HTTPException
from app.models.export_request import ExportRequest
from app.services.audit import log_event
from app.services.export_jobs import create_export_job


def request_export(*, db, snapshot, user, export_type, options):
    """
    Phase M.1 canonical export request entrypoint.

    Responsibilities:
    - validate snapshot
    - persist ExportRequest (FK root)
    - journal request
    - create exactly one ExportJob
    """

    if snapshot.status != "completed":
        raise HTTPException(409, "Snapshot not exportable")

    # 1️⃣ Create ExportRequest (FK root)
    export_request = ExportRequest(
        project_id=snapshot.project_id,
        snapshot_id=snapshot.id,
        export_type=export_type,
        options=options,
        status="accepted",
    )

    db.add(export_request)
    db.commit()
    db.refresh(export_request)

    # 2️⃣ Journal (user attribution lives here)
    log_event(
        db=db,
        user_id=user.id,
        action="export.requested",
        resource_type="export_request",
        resource_id=export_request.id,
    )

    # 3️⃣ Create ExportJob (exactly one)
    job = create_export_job(
        db=db,
        export_request=export_request,
        project_id=export_request.project_id,
    )

    return export_request, job

