import pytest
from fastapi import HTTPException
from app.studio.guards import require_station
from app.studio.stations import StudioStation

def test_tool_blocked_outside_station():
    with pytest.raises(HTTPException):
        require_station(
            current_station=StudioStation.review,
            allowed={StudioStation.geometry},
        )

