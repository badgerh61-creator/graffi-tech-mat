def apply_body_morph(
    *,
    base_state: dict | None,
    preset: dict,
    parameters: dict,
) -> dict:
    """
    Phase K.3 — deterministic body morph application.
    Pure function.
    """

    state = dict(base_state or {})

    width = parameters.get(
        "width_factor",
        preset["defaults"]["width_factor"],
    )

    # Apply directly to body_state (NO extra nesting)
    state["width_factor"] = width

    return state

