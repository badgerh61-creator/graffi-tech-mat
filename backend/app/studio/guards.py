from fastapi import HTTPException
from app.studio.stations import StudioStation

def require_station(
    *,
    current_station: StudioStation,
    allowed: set[StudioStation],
):
    if current_station not in allowed:
        raise HTTPException(
            status_code=403,
            detail=f"Operation not allowed in station {current_station}",
        )

