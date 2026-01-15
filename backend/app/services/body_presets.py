# Phase K.3 — Body morph presets
# ❗ Read-only
# ❗ Deterministic
# ❗ No DB
# ❗ No side effects

BODY_MORPH_PRESETS = {
    "widebody_v1": {
        # Panels that MUST exist on the snapshot
        "required_panels": {
            "fender_front_left",
            "fender_front_right",
            "fender_rear_left",
            "fender_rear_right",
        },
        "defaults": {
            "width_factor": 1.15,
        },
        "limits": {
            "width_factor": (1.05, 1.30),
        },
    },

    "truck_only_widebody": {
        # Trucks require rear panels that normal cars don't have
        "required_panels": {
            "fender_front_left",
            "fender_front_right",
            "fender_rear_left",
            "fender_rear_right",
            "bumper_rear",
        },
        "defaults": {
            "width_factor": 1.20,
        },
        "limits": {
            "width_factor": (1.10, 1.40),
        },
    },
}


def get_body_morph_preset(preset_id: str):
    """
    Phase K.3:
    Pure preset lookup. No validation, no mutation.
    """
    return BODY_MORPH_PRESETS.get(preset_id)

