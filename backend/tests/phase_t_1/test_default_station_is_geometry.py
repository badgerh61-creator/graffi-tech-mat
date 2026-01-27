from app.studio.session import StudioSession
from app.studio.stations import StudioStation

def test_default_station_is_geometry():
    session = StudioSession(user_id=1)
    assert session.station == StudioStation.geometry

