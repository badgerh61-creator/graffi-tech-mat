import io
import json
import hashlib
import zipfile
from app.models.zip_artifact import ZipArtifact

GENERATOR_VERSION = "m5-stub-1"

def build_export_zip(*, export_request_id, snapshot_id, artifacts):
    buffer = io.BytesIO()

    # deterministic zip: no timestamps
    with zipfile.ZipFile(
        buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        strict_timestamps=True,
    ) as zf:

        manifest_files = []

        for artifact in sorted(artifacts, key=lambda a: a.path):
            zf.writestr(artifact.path, artifact.bytes)

            manifest_files.append({
                "path": artifact.path,
                "sha256": hashlib.sha256(artifact.bytes).hexdigest(),
            })

        manifest = {
            "export_request_id": export_request_id,
            "snapshot_id": snapshot_id,
            "generator_version": GENERATOR_VERSION,
            "files": manifest_files,
        }

        zf.writestr(
            "manifest.json",
            json.dumps(manifest, sort_keys=True).encode("utf-8"),
        )

    return ZipArtifact(bytes=buffer.getvalue())

