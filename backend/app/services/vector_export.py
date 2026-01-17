import hashlib
from app.models.export_artifact import ExportArtifact

SUPPORTED_VECTOR_FORMATS = {"svg", "pdf", "eps"}

def run_vector_export(*, db, snapshot, options):
    fmt = options.get("format")
    if fmt not in SUPPORTED_VECTOR_FORMATS:
        raise ValueError("Unsupported vector format")

    # ✅ FIX: use real snapshot field
    payload = f"VECTOR:{snapshot.scene_state_hash}:{fmt}:{options}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact(
        bytes=payload,
        hash=digest,
        format=fmt,
    )

