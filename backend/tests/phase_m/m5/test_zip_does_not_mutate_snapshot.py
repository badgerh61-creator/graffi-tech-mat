from app.services.zip_packager import build_export_zip

def test_zip_packaging_does_not_touch_snapshot(
    completed_snapshot,
    artifacts,
):
    before = completed_snapshot.scene_state_hash

    build_export_zip(
        export_request_id="req-1",
        snapshot_id=completed_snapshot.id,
        artifacts=artifacts,
    )

    assert completed_snapshot.scene_state_hash == before


