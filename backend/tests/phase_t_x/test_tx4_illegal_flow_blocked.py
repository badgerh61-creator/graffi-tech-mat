import pytest
from app.studio import execute_tool

def test_illegal_flow_blocked(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(Exception) as exc:
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=draft_snapshot,
            station="finalization",
            tool="finalize",
            operation="finalize",
            params={},
        )

    assert "flow" in str(exc.value)

