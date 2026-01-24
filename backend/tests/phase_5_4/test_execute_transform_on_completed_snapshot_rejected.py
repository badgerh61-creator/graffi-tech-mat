import pytest
from fastapi import HTTPException

from app.services.snapshot_mutations import apply_transform

def test_execute_transform_on_completed_snapshot_rejected(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_transform(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
            operation="translate",
            target_id="panel-1",
            params={"x": 5},
        )

    assert exc.value.status_code == 409

