import pytest
from fastapi import HTTPException
from app.studio.session import StudioSession
from app.studio.stations import StudioStation

def test_illegal_station_transition_rejected():
    session = StudioSession(user_id=1)

    with pytest.raises(HTTPException) as exc:
        session.set_station(StudioStation.review)

    assert exc.value.status_code == 409

