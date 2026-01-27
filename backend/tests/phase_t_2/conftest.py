import pytest

@pytest.fixture
def editor_capabilities():
    """
    Canonical editor capability set for Phase T tests.
    Phase T does NOT compute capabilities — it only enforces them.
    """
    return {
        "canEditGeometry": True,
        "canFinalizeSnapshot": True,
    }

