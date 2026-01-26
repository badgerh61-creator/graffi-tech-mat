import pytest
from app.services import apply_panel_parameters
from fastapi import HTTPException

def test_panel_parameters_on_completed_snapshot_rejected(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_panel_parameters(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
            panel_id="panel-1",
            parameters={"length_offset": 50},
        )

    assert exc.value.status_code == 409

