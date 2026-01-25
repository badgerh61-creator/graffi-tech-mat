import pytest
from fastapi import HTTPException
from app.services.curve_constraints import add_curve_constraint

def test_invalid_constraint_type_rejected(
    db,
    draft_snapshot,
    curve,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        add_curve_constraint(
            db=db,
            snapshot=draft_snapshot,
            curve=curve,
            user=editor_user,
            constraint_type="colinear",
            reference=None,
            params={},
        )

    assert exc.value.status_code == 422

