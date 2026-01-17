from app.services.vector_export import run_vector_export

def test_vector_export_does_not_mutate_snapshot(
    db,
    completed_snapshot,
):
    before = completed_snapshot.scene_state_hash

    run_vector_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "svg", "include_layers": False},
    )

    assert completed_snapshot.scene_state_hash == before

