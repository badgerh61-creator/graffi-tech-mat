from enum import Enum
from fastapi import HTTPException

class StudioStation(str, Enum):
    geometry = "geometry"
    curve = "curve"
    panel = "panel"
    validation = "validation"
    review = "review"


# Authoritative station transitions (can be extended later)
ALLOWED_STATION_TRANSITIONS = {
    StudioStation.geometry: {
        StudioStation.curve,
        StudioStation.panel,
    },
    StudioStation.curve: {
        StudioStation.geometry,
        StudioStation.panel,
    },
    StudioStation.panel: {
        StudioStation.validation,
        StudioStation.geometry,
    },
    StudioStation.validation: {
        StudioStation.review,
        StudioStation.panel,
    },
    StudioStation.review: set(),
}


def assert_valid_station_transition(
    *,
    from_station: StudioStation,
    to_station: StudioStation,
):
    if to_station not in ALLOWED_STATION_TRANSITIONS.get(from_station, set()):
        raise HTTPException(
            status_code=409,
            detail=f"Illegal station transition: {from_station} → {to_station}",
        )

