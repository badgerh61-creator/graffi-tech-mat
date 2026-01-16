from app.services.image_export import run_image_export


def test_image_export_is_deterministic(
    db,
    completed_snapshot,
    export_job,
):
    output1 = run_image_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "png"},
    )

    output2 = run_image_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "png"},
    )

    assert output1.hash == output2.hash

