from app.services.snapshot_mutations import apply_transform

def test_execute_transform_success(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot = apply_transform(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="translate",
        target_id="panel-1",
        params={"x": 10},
    )

    assert new_snapshot.id != draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert new_snapshot.status == "draft"

