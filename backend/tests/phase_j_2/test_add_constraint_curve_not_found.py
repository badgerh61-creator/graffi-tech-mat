import pytest
from fastapi import HTTPException
from app.services.curve_constraints import add_curve_constraint

def test_add_constraint_curve_not_found(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        add_curve_constraint(
            db=db,
            snapshot=draft_snapshot,
            curve=None,
            user=editor_user,
            constraint_type="horizontal",
            reference=None,
            params={},
        )

    assert exc.value.status_code == 404

