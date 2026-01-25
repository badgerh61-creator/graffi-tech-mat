import pytest
from fastapi import HTTPException
from app.services.curve_creator import create_curve

def test_create_curve_on_completed_snapshot_rejected(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        create_curve(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
            curve_type="line",
            reference_plane_id="front",
            params={},
            constraints=[],
        )

    assert exc.value.status_code == 409

