from app.services.image_export import run_image_export


def test_image_export_does_not_mutate_snapshot(
    db,
    completed_snapshot,
):
    before_id = completed_snapshot.id
    before_status = completed_snapshot.status
    before_created_at = completed_snapshot.created_at

    run_image_export(
        db=db,
        snapshot=completed_snapshot,
        options={"format": "png"},
    )

    db.refresh(completed_snapshot)

    assert completed_snapshot.id == before_id
    assert completed_snapshot.status == before_status
    assert completed_snapshot.created_at == before_created_at

