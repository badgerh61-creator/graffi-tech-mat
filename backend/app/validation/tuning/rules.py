def validate_wheel_parameters(*, diameter, width, offset):
    """
    Deterministic, data-only validation.
    No physics. No vehicle-specific logic yet.
    """

    if not isinstance(diameter, (int, float)) or not (14 <= diameter <= 24):
        return False, "Invalid wheel diameter"

    if not isinstance(width, (int, float)) or not (5 <= width <= 14):
        return False, "Invalid wheel width"

    if not isinstance(offset, (int, float)) or not (-50 <= offset <= 60):
        return False, "Invalid wheel offset"

    return True, None

