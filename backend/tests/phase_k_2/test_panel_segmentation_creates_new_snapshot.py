from app.services.panel_segmenter import segment_panels

def test_panel_segmentation_creates_new_snapshot(
    db,
    surfaced_draft_snapshot,
    editor_user,
):
    new_snapshot = segment_panels(
        db=db,
        snapshot=surfaced_draft_snapshot,
        user=editor_user,
        panels=[{
            "type": "door",
            "surface_ids": ["surface-1"],
            "label": "front-left-door",
        }],
    )

    assert new_snapshot.id != surfaced_draft_snapshot.id
    assert new_snapshot.parent_snapshot_id == surfaced_draft_snapshot.id
    assert new_snapshot.status == "draft"

