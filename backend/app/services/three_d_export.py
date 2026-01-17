import hashlib
from app.models.export_artifact import ExportArtifact

SUPPORTED_3D_FORMATS = {"glb", "gltf"}

def run_3d_export(*, db, snapshot, options):
    fmt = options.get("format")
    if fmt not in SUPPORTED_3D_FORMATS:
        raise ValueError("Unsupported 3D format")

    include_materials = options.get("include_materials", True)
    include_textures = options.get("include_textures", True)

    payload = (
        f"3D:{snapshot.scene_state_hash}:{fmt}:"
        f"materials={include_materials}:"
        f"textures={include_textures}"
    ).encode("utf-8")

    digest = hashlib.sha256(payload).hexdigest()

    return ExportArtifact(
        bytes=payload,
        hash=digest,
        format=fmt,
    )

