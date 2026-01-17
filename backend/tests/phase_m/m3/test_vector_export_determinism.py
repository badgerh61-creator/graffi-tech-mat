from app.services.vector_export import run_vector_export

def test_vector_export_is_deterministic(
    db,
    completed_snapshot,
):
    out1 = run_vector_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "svg", "include_layers": True},
    )

    out2 = run_vector_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "svg", "include_layers": True},
    )

    assert out1.hash == out2.hash

