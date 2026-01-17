from app.services.zip_packager import build_export_zip

import json
import hashlib

def test_manifest_hashes_match(
    artifacts,
):
    zip_artifact = build_export_zip(
        export_request_id="req-1",
        snapshot_id="snap-1",
        artifacts=artifacts,
    )

    manifest = json.loads(zip_artifact.read("manifest.json"))

    for entry in manifest["files"]:
        content = zip_artifact.read(entry["path"])
        digest = hashlib.sha256(content).hexdigest()
        assert digest == entry["sha256"]

