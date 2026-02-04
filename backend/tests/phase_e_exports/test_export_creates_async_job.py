from app.services.image_exporter import create_image_export

def test_export_creates_async_job(
    db,
    completed_snapshot,
    editor_user,
):
    export = create_image_export(
        db=db,
        snapshot=completed_snapshot,
        user=editor_user,
        format="jpeg",
        resolution="low",
    )

    assert export.job_id is not None

