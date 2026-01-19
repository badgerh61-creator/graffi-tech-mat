import hashlib
from app.models.export_artifact import ExportArtifact

SUPPORTED_FORMATS = {"png", "jpg", "tiff"}

def run_image_export(*, db, snapshot, options):
    fmt = options.get("format", "png")
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported format")

    camera_id = options.get("camera_id")
    if camera_id:
        raise ValueError("Invalid camera")

    payload = f"{snapshot.id}:{fmt}:{options}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact.completed(
        bytes=payload,
        hash=digest,
        format=fmt,
        snapshot_id=snapshot.id,
    )

