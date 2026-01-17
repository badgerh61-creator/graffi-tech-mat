from app.services.zip_packager import build_export_zip

def test_zip_contains_expected_files(
    artifacts,
):
    zip_artifact = build_export_zip(
        export_request_id="req-1",
        snapshot_id="snap-1",
        artifacts=artifacts,
    )

    names = zip_artifact.namelist()

    assert "manifest.json" in names
    assert "render.png" in names
    assert "print/design.tiff" in names

