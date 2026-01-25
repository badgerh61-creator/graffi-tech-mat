import pytest
from app.services import generate_surfaces_for_snapshot
from fastapi import HTTPException

def test_completed_snapshot_rejected(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException):
        generate_surfaces_for_snapshot(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
        )

