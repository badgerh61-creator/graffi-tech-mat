# backend/app/services/tuning_presets.py

# Phase K.2 — READ-ONLY tuning presets
# ❗ No DB
# ❗ No randomness
# ❗ No side effects


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


ENGINE_TUNE_PRESETS = {
    "eco": {
        "torque_bias": -10,
    },
    "stock": {
        "torque_bias": 0,
    },
    "sport": {
        "torque_bias": 10,
    },
    "race": {
        "torque_bias": 20,
    },
}


# -------------------------------------------------
# Phase K.2 — Brakes presets (read-only)
# -------------------------------------------------

_BRAKE_PRESETS = {
    "stock": {
        "bias": "balanced",
        "force": "standard",
    },
    "sport": {
        "bias": "front",
        "force": "high",
    },
    "track": {
        "bias": "front",
        "force": "max",
    },
}


def get_suspension_preset(preset_id: str):
    """
    Phase K.2 — read-only suspension preset lookup.
    """
    return SUSPENSION_PRESETS.get(preset_id)


def get_engine_tune_preset(preset_id: str):
    """
    Phase K.2 — read-only engine tune preset lookup.
    """
    return ENGINE_TUNE_PRESETS.get(preset_id)


def get_brake_preset(preset_id: str):
    """
    Resolve a brakes preset by ID.
    Phase K.2 — deterministic, read-only.
    """
    return _BRAKE_PRESETS.get(preset_id)
