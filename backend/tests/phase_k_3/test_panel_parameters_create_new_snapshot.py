from app.services import apply_panel_parameters

def test_panel_parameters_create_new_snapshot(
    db,
    segmented_draft_snapshot,
    editor_user,
):
    new_snapshot = apply_panel_parameters(
        db=db,
        snapshot=segmented_draft_snapshot,
        user=editor_user,
        panel_id="panel-1",
        parameters={"length_offset": 100},
    )

    assert new_snapshot.id != segmented_draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == segmented_draft_snapshot.id
    assert new_snapshot.status == "draft"

