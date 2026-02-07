import pytest
from fastapi import HTTPException

def test_decor_edit_on_completed_snapshot_blocked(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_decor_change(
            db=db,
            snapshot=completed_snapshot,
            user=editor_user,
            operation="decor.apply_material",
            target_id="panel-1",
            params={},
        )

    assert exc.value.status_code == 409

