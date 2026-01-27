import pytest
from fastapi import HTTPException
from app.services.tool_guard import require_tool_allowed
from app.studio.stations import StudioStation

def test_tool_blocked_by_missing_capability(draft_snapshot):
    with pytest.raises(HTTPException) as exc:
        require_tool_allowed(
            tool_name="translate",
            snapshot=draft_snapshot,
            station=StudioStation.geometry,
            capabilities={},  # no permissions
        )

    assert exc.value.status_code == 403

