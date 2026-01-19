import uuid
import pytest
from app.services.geometry_validator import validate_geometry

class TestSurface:
    def __init__(
        self,
        *,
        violates_curvature=False,
        self_intersecting=False,
        is_symmetric=True,
    ):
        self.id = str(uuid.uuid4())
        self.violates_curvature = violates_curvature
        self.self_intersecting = self_intersecting
        self.is_symmetric = is_symmetric


class TestPanel:
    def __init__(
        self,
        *,
        overlaps=False,
        continuous=True,
    ):
        self.id = str(uuid.uuid4())
        self.overlaps = overlaps
        self.continuous = continuous


# ---------- SURFACE FIXTURES ----------

@pytest.fixture
def invalid_curvature_surface():
    return TestSurface(violates_curvature=True)


@pytest.fixture
def self_intersecting_surface():
    return TestSurface(self_intersecting=True)


@pytest.fixture
def asymmetric_surface():
    return TestSurface(is_symmetric=False)


@pytest.fixture
def valid_surfaces():
    return [
        TestSurface(),
        TestSurface(),
    ]


# ---------- PANEL FIXTURES ----------

@pytest.fixture
def overlapping_panels():
    return [
        TestPanel(overlaps=True),
        TestPanel(overlaps=True),
    ]


@pytest.fixture
def discontinuous_panels():
    return [
        TestPanel(continuous=False),
        TestPanel(continuous=False),
    ]


@pytest.fixture
def valid_panels():
    return [
        TestPanel(),
        TestPanel(),
    ]


__all__ = ["validate_geometry"]

