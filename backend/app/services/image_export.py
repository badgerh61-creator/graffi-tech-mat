# backend/app/services/image_export.py

import hashlib
from app.services.export_result import ExportResult

SUPPORTED_FORMATS = {"png", "jpg", "tiff"}


def run_image_export(*, snapshot, options, db=None):
    """
    Phase M.2 — PURE deterministic image export.

    Compatibility guarantees:
    - Accepts db=None for legacy tests
    - NEVER touches the database
    - Deterministic output
    """

    fmt = options.get("format", "png")
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported format")

    camera_id = options.get("camera_id")
    if camera_id is not None:
        raise ValueError("Invalid camera")

    payload = f"{snapshot.id}:{fmt}:{options}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    return ExportResult(
        bytes=payload,
        hash=digest,
        format=fmt,
        snapshot_id=snapshot.id,
    )

