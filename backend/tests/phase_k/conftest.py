import pytest

from app.models.surface import Surface


class DummyCurve:
    """
    Minimal curve stub for Phase K tests.

    This is a PURE test object:
    - No DB
    - No engine
    - No geometry math
    """

    def __init__(self, id: str, is_symmetric: bool = True):
        self.id = id
        self.is_symmetric = is_symmetric


@pytest.fixture
def curve_set():
    """
    Canonical symmetric curve set for Level-2 surface generation.
    """
    return [
        DummyCurve(id="curve-a"),
        DummyCurve(id="curve-b"),
    ]


@pytest.fixture
def asymmetric_curve_set():
    """
    Curve set with explicit asymmetry (used by symmetry tests).
    """
    return [
        DummyCurve(id="curve-a", is_symmetric=False),
        DummyCurve(id="curve-b"),
    ]


@pytest.fixture
def params():
    """
    Canonical Level-2 parametric controls.

    REQUIRED by:
    - test_surface_generation_is_deterministic
    """
    return {
        "length": 4.2,
        "height": 1.6,
        "width": 1.8,
        "rake": 12,
        "roof_arc": 0.35,
    }


@pytest.fixture
def surface(curve_set, params):
    """
    Canonical Level-2 Surface fixture.

    Guarantees:
    - Stable identity
    - Deterministic hash
    - No DB or engine coupling
    """

    return Surface(
        source_curves=curve_set,
        params=params,
        method="loft",
    )

