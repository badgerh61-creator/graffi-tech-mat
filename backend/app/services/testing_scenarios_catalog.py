from __future__ import annotations
from typing import Dict, List, Optional

# Hard-coded catalog (v1). Later you can version it or store it in DB.
_SCENARIOS: List[Dict[str, object]] = [
    {
        "id": "track-dry-day-v1",
        "name": "Track — Dry Day",
        "category": "track",
        "surface": "asphalt",
        "weather": "sunny",
        "camera_preset_id": "cam-track-v1",
        "lighting_preset_id": "light-noon-v1",
        "version": 1,
    },
    {
        "id": "city-wet-night-v1",
        "name": "City — Wet Night",
        "category": "city",
        "surface": "wet",
        "weather": "night",
        "camera_preset_id": "cam-city-v1",
        "lighting_preset_id": "light-night-wet-v1",
        "version": 1,
    },
    {
        "id": "highway-dry-day-v1",
        "name": "Highway — Dry Day",
        "category": "highway",
        "surface": "asphalt",
        "weather": "sunny",
        "camera_preset_id": "cam-highway-v1",
        "lighting_preset_id": "light-noon-v1",
        "version": 1,
    },
]

def list_scenarios() -> List[Dict[str, object]]:
    return list(_SCENARIOS)

def get_scenario(scenario_id: str) -> Optional[Dict[str, object]]:
    for s in _SCENARIOS:
        if s["id"] == scenario_id:
            return dict(s)
    return None
