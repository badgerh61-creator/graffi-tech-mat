import pytest
from fastapi import HTTPException
from app.services.snapshot_mutations import apply_transform

def test_execute_transform_invalid_operation(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_transform(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user,
            operation="shear",
            target_id="panel-1",
            params={},
        )

    assert exc.value.status_code == 422

