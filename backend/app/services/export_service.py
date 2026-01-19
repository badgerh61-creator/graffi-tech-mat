# backend/app/services/export_service.py

import hashlib
from app.models.export_artifact import ExportArtifact
from app.services.export_serialization import serialize_snapshot_for_export

def export_snapshot(*, snapshot, format):
    if snapshot.status != "completed":
        return ExportArtifact.failed(
            format=format,
            snapshot_id=snapshot.id,
        )

    payload = serialize_snapshot_for_export(
        snapshot=snapshot,
        format=format,
    )

    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact.completed(
        bytes=payload,
        hash=digest,
        format=format,
        snapshot_id=snapshot.id,
    )

