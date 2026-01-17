from app.services.zip_packager import build_export_zip

def test_zip_is_deterministic(artifacts):
    zip1 = build_export_zip(
        export_request_id="req-1",
        snapshot_id="snap-1",
        artifacts=artifacts,
    )

    zip2 = build_export_zip(
        export_request_id="req-1",
        snapshot_id="snap-1",
        artifacts=artifacts,
    )

    assert zip1.bytes == zip2.bytes

