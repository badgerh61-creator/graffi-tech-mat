from app.services.three_d_export import run_3d_export

def test_3d_export_is_static_only(
    db,
    completed_snapshot,
):
    artifact = run_3d_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "glb"},
    )

    assert b"ANIMATION" not in artifact.bytes
    assert b"PHYSICS" not in artifact.bytes

