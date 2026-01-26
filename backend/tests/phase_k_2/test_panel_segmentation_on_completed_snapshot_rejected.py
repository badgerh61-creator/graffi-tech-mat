import pytest
from app.services.panel_segmenter import segment_panels
from fastapi import HTTPException

def test_panel_segmentation_on_completed_snapshot_rejected(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        segment_panels(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
            panels=[],
        )

    assert exc.value.status_code == 409

