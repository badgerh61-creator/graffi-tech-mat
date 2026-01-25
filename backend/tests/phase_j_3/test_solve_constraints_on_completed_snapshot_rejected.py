import pytest
from app.services.constraint_solver import solve_constraints
from fastapi import HTTPException

def test_solve_constraints_on_completed_snapshot_rejected(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        solve_constraints(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
        )

    assert exc.value.status_code == 409

