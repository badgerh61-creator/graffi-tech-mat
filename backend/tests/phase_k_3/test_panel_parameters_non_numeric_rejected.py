import pytest
from app.services import apply_panel_parameters
from fastapi import HTTPException

def test_panel_parameters_non_numeric_rejected(
    db,
    segmented_draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_panel_parameters(
            db=db,
            snapshot=segmented_draft_snapshot,
            user=editor_user,
            panel_id="panel-1",
            parameters={"length_offset": "big"},
        )

    assert exc.value.status_code == 422

