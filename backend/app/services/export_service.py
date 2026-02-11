# backend/app/services/export_service.py

import hashlib
from app.models.export_artifact import ExportArtifact
from app.services.export_serialization import serialize_snapshot_for_export
import app.observability.metrics as metrics_module


def export_snapshot(*, snapshot, format):
    """
    Phase M legacy export compatibility layer.
    Removed in Phase N.
    """


    # 🔢 Phase P observability
    metrics_module.metrics.inc("export.attempt.count")
    
    if snapshot.status != "completed":
        return ExportArtifact.failed(
            format=format,
            snapshot_id=snapshot.id,
            export_job_id=None,
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
        export_job_id=None,
    )

