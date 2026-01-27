import pytest
from app.studio import execute_tool

def test_invalid_station_blocks_execution(
    db,
    draft_snapshot,
    editor_user,
):
    with pytest.raises(Exception) as exc:
        execute_tool(
            db=db,
            user=editor_user,
            snapshot=draft_snapshot,
            station="review",  # illegal
            tool="transform",
            operation="translate",
            params={"x": 5},
        )

    assert "station" in str(exc.value)

