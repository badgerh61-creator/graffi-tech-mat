import pytest
from app.studio import execute_tool

def test_invalid_tool_rejected(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(Exception) as exc:
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=draft_snapshot,
            station="geometry",
            tool="shear",
            operation="shear",
            params={},
        )

    assert "tool" in str(exc.value)

