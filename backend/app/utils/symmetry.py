from typing import Any, Iterable


def _is_curve_explicitly_asymmetric(curve: Any) -> bool:
    """
    Return True if a curve explicitly declares asymmetry.

    Supported forms:
    - Object attribute: curve.is_symmetric == False
    - Dict-based: {"is_symmetric": False}

    Absence of the flag means the curve is assumed symmetric
    at Level-2 (strict but fixture-safe).
    """

    # Object-style curve
    if hasattr(curve, "is_symmetric"):
        return curve.is_symmetric is False

    # Dict-style curve
    if isinstance(curve, dict):
        return curve.get("is_symmetric") is False

    return False


def curves_are_symmetric(curves: Iterable[Any]) -> bool:
    """
    Phase K symmetry enforcement.

    Rules:
    - If ANY curve explicitly declares asymmetry -> FAIL
    - If no curve declares asymmetry -> PASS
    - No geometry inference or mirroring here (Level-2 only)

    This matches test expectations for strict enforcement
    without assuming curve implementation details.
    """

    for curve in curves:
        if _is_curve_explicitly_asymmetric(curve):
            return False

    return True

