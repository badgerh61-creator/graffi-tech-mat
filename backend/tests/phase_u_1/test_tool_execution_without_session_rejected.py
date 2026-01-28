import pytest
from fastapi import HTTPException
from app.services.transform_executor import apply_transform

def test_tool_execution_without_session_rejected(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(HTTPException) as exc:
        apply_transform(
            db=db,
            snapshot=draft_snapshot,
            user=editor_user,
            operation="translate",
            target_id="panel-1",
            params={"x": 1},
        )

    assert exc.value.status_code == 403

