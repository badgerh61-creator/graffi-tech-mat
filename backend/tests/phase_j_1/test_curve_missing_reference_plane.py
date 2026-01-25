import pytest
from fastapi import HTTPException
from app.services.curve_creator import create_curve

def test_curve_missing_reference_plane(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        create_curve(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user,
            curve_type="line",
            reference_plane_id=None,
            params={"x1": 0, "y1": 0, "x2": 10, "y2": 0},
            constraints=[],
        )

    assert exc.value.status_code == 400

