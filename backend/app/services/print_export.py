import hashlib
from app.models.export_artifact import ExportArtifact

SUPPORTED_PRINT_FORMATS = {"tiff", "pdf"}

def run_print_export(*, db, snapshot, options):
    fmt = options.get("format")
    dpi = options.get("dpi")
    units = options.get("units")
    profile = options.get("color_profile")

    if fmt not in SUPPORTED_PRINT_FORMATS:
        raise ValueError("Unsupported print format")

    if not dpi or not units or not profile:
        raise ValueError("Missing required print options")

    payload = f"PRINT:{snapshot.scene_hash}:{fmt}:{dpi}:{units}:{profile}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact(
        bytes=payload,
        hash=digest,
        format=fmt,
    )

