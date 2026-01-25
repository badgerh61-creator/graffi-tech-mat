import pytest
from fastapi import HTTPException
from app.services.curve_creator import create_curve

def test_invalid_curve_type_rejected(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        create_curve(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user,
            curve_type="spline",
            reference_plane_id="front",
            params={},
            constraints=[],
        )

    assert exc.value.status_code == 422

