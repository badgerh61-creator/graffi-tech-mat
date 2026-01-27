import pytest
from app.studio import execute_tool

def test_mode_violation_blocked(
    db,
    completed_snapshot,
    editor_user,
):
    with pytest.raises(Exception) as exc:
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=completed_snapshot,
            station="geometry",
            tool="transform",
            operation="translate",
            params={"x": 1},
        )

    assert "mode" in str(exc.value)

