# backend/app/services/three_d_export.py

import hashlib
from app.models.export_artifact import ExportArtifact

SUPPORTED_3D_FORMATS = {"glb", "gltf"}


def run_3d_export(*, db, snapshot, options):
    fmt = options.get("format")
    if fmt not in SUPPORTED_3D_FORMATS:
        raise ValueError("Unsupported 3D format")

    # Phase M rule: STATIC ONLY
    payload = f"3D:{snapshot.scene_state_hash}:{fmt}:static".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact.completed(
        bytes=payload,
        hash=digest,
        format=fmt,
        snapshot_id=snapshot.id,
        export_job_id=None,
    )

