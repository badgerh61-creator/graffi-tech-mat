from app.studio.session import StudioSession
from app.studio.stations import StudioStation

def test_legal_station_transition():
    session = StudioSession(user_id=1)

    session.set_station(StudioStation.curve)
    assert session.station == StudioStation.curve

