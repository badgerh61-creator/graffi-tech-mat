from fastapi import HTTPException
from app.studio.stations import (
    StudioStation,
    assert_valid_station_transition,
)

class StudioSession:
    """
    Authoritative studio session.
    Not UI state. Not client-trusted.
    """

    def __init__(self, *, user_id: int):
        self.user_id = user_id
        self.station: StudioStation = StudioStation.geometry

    def set_station(self, station: StudioStation):
        assert_valid_station_transition(
            from_station=self.station,
            to_station=station,
        )
        self.station = station

