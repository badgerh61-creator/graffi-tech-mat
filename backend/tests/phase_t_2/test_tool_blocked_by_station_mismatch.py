import pytest
from fastapi import HTTPException
from app.services.tool_guard import require_tool_allowed
from app.studio.stations import StudioStation

def test_tool_blocked_by_station_mismatch(
    draft_snapshot,
    editor_capabilities,
):
    with pytest.raises(HTTPException) as exc:
        require_tool_allowed(
            tool_name="translate",
            snapshot=draft_snapshot,
            station=StudioStation.review,
            capabilities=editor_capabilities,
        )

    assert exc.value.status_code == 409

