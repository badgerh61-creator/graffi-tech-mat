import pytest
from fastapi import HTTPException
from app.services.tool_guard import require_tool_allowed

def test_unknown_tool_rejected(draft_snapshot, editor_user):
    with pytest.raises(HTTPException) as exc:
        require_tool_allowed(
            tool_name="warp",
            snapshot=draft_snapshot,
            station=None,
            capabilities={},
        )

    assert exc.value.status_code == 404

