from app.services import apply_panel_parameters

def test_panel_parameters_invalid_panel_fails(
    db,
    segmented_draft_snapshot,
    editor_user,
):
    failed = apply_panel_parameters(
        db=db,
        snapshot=segmented_draft_snapshot,
        user=editor_user,
        panel_id="missing-panel",
        parameters={"length_offset": 50},
    )

    assert failed.status == "failed"

