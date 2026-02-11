# backend/app/services/vector_export.py

import hashlib
from app.models.export_artifact import ExportArtifact

SUPPORTED_VECTOR_FORMATS = {"svg", "pdf"}


def run_vector_export(*, db, snapshot, options):
    fmt = options.get("format")
    if fmt not in SUPPORTED_VECTOR_FORMATS:
        raise ValueError("Unsupported vector format")

    payload = f"VECTOR:{snapshot.scene_state_hash}:{fmt}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact.completed(
        bytes=payload,
        hash=digest,
        format=fmt,
        snapshot_id=snapshot.id,
        export_job_id=None,  # Phase M allows non-job artifacts
    )

