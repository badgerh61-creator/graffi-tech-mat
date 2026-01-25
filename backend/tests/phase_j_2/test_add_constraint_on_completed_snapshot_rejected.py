import pytest
from fastapi import HTTPException
from app.services.curve_constraints import add_curve_constraint

def test_add_constraint_on_completed_snapshot_rejected(
    db,
    completed_snapshot,
    curve,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        add_curve_constraint(
            db=db,
            snapshot=completed_snapshot,
            curve=curve,
            user=editor_user,
            constraint_type="horizontal",
            reference=None,
            params={},
        )

    assert exc.value.status_code == 409

