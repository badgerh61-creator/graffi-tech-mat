def test_decor_edit_creates_new_snapshot(
    db,
    draft_snapshot,
    editor_user,
):
    new_snapshot = apply_decor_change(
        db=db,
        snapshot=draft_snapshot,
        user=editor_user,
        operation="decor.apply_material",
        target_id="panel-1",
        params={"material": "leather"},
    )

    assert new_snapshot.id != draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == draft_snapshot.id
    assert new_snapshot.status == "draft"

