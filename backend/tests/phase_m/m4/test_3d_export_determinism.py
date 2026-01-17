# tests/phase_m/m4/test_3d_export_determinism.py

from app.services.three_d_export import run_3d_export


def test_3d_export_is_deterministic(
    db,
    completed_snapshot,
):
    out1 = run_3d_export(
        db=db,
        snapshot=completed_snapshot,
        options={
            "format": "glb",
            "include_materials": True,
            "include_textures": True,
        },
    )

    out2 = run_3d_export(
        db=db,
        snapshot=completed_snapshot,
        options={
            "format": "glb",
            "include_materials": True,
            "include_textures": True,
        },
    )

    assert out1.hash == out2.hash


