from app.services.three_d_export import run_3d_export

def test_3d_export_does_not_mutate_snapshot(
    db,
    completed_snapshot,
):
    before = completed_snapshot.scene_state_hash

    run_3d_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "gltf"},
    )

    assert completed_snapshot.scene_state_hash == before


