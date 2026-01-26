from app.services.panel_segmenter import segment_panels

def test_panels_attached_to_snapshot(
    db,
    surfaced_draft_snapshot,
    editor_user,
):
    new_snapshot = segment_panels(
        db=db,
        snapshot=surfaced_draft_snapshot,
        user=editor_user,
        panels=[{
            "type": "roof",
            "surface_ids": ["surface-1"],
            "label": "main-roof",
        }],
    )

    assert len(new_snapshot.panels) == 1

