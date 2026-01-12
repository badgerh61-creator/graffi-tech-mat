# backend/app/services/tuning_presets.py

SUSPENSION_PRESETS = {
    "sport_low": {
        "ride_height_mm": -20,
    },
    "comfort_stock": {
        "ride_height_mm": 0,
    },
    "offroad_high": {
        "ride_height_mm": 30,
    },
}


def get_suspension_preset(preset_id: str):
    """
    Phase K.2 — read-only preset lookup.

    ❗ No DB
    ❗ No randomness
    ❗ No side effects
    """
    return SUSPENSION_PRESETS.get(preset_id)

