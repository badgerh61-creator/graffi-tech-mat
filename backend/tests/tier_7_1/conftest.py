import pytest


@pytest.fixture
def geometry_station():
    return "geometry"


@pytest.fixture
def translate_request_payload():
    return {
        "target_id": "panel-1",
        "params": {"x": 10, "y": 0, "z": 0},
    }
