# backend/app/services/export_service.py

import hashlib

from app.models.export_artifact import ExportArtifact
from app.services.export_serialization import serialize_snapshot_for_export

# 🔍 Phase P — observability (import module, not variable)
import app.observability.metrics as metrics_module


def export_snapshot(*, snapshot, format):
    metrics_module.metrics.inc("export.attempt.count")

    if snapshot.status != "completed":
        metrics_module.metrics.inc("export.failure.count")
        return ExportArtifact.failed(
            format=format,
            snapshot_id=snapshot.id,
        )

    payload = serialize_snapshot_for_export(
        snapshot=snapshot,
        format=format,
    )

    digest = hashlib.sha256(payload).hexdigest()

    metrics_module.metrics.inc("export.success.count")

    return ExportArtifact.completed(
        bytes=payload,
        hash=digest,
        format=format,
        snapshot_id=snapshot.id,
    )

