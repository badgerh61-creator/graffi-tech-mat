from app.services.panel_segmenter import segment_panels

def test_panel_segmentation_invalid_surface_fails(
    db,
    surfaced_draft_snapshot,
    editor_user,
):
    failed = segment_panels(
        db=db,
        snapshot=surfaced_draft_snapshot,
        user=editor_user,
        panels=[{
            "type": "door",
            "surface_ids": ["missing-surface"],
            "label": "bad-panel",
        }],
    )

    assert failed.status == "failed"

