def apply_suspension_preset(
    *,
    base_state: dict,
    preset: dict,
) -> dict:
    """
    Phase K.2 — STEP 4

    Deterministically apply suspension preset
    to existing tuning state.

    ❗ Pure function
    ❗ No randomness
    ❗ No side effects
    """

    next_state = dict(base_state)

    next_state["suspension"] = {
        "ride_height_mm": preset["ride_height_mm"],
    }

    return next_state

