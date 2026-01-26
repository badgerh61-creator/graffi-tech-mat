import pytest
from app.services import segment_panels

@pytest.fixture
def segmented_draft_snapshot(
    db,
    surfaced_draft_snapshot,
    editor_user,
):
    """
    Draft snapshot with explicit surfaces grouped into panels.
    Required invariant for Phase K.3.
    """

    # ✅ AUTHORITATIVE SOURCE OF SURFACES
    surfaces = surfaced_draft_snapshot.surfaces

    assert surfaces, "Phase K.1 invariant violated: no surfaces present"

    surface_ids = [surface["id"] for surface in surfaces]

    panels = [
        {
            "id": "panel-1",
            "type": "door",
            "side": "left",
            "surface_ids": surface_ids[: len(surface_ids) // 2],
        },
        {
            "id": "panel-2",
            "type": "roof",
            "side": "center",
            "surface_ids": surface_ids[len(surface_ids) // 2 :],
        },
    ]

    segmented_snapshot = segment_panels(
        db=db,
        snapshot=surfaced_draft_snapshot,
        user=editor_user,
        panels=panels,
    )

    return segmented_snapshot

