import pytest
from app.validation.decor.exterior import validate_apply_decal
from app.validation.decor.errors import CapabilityRequired


class FakeSnapshot:
    status = "completed"
    is_obsolete = False
    vehicle_panels = {"door_left", "door_right"}


class FakeDecal:
    is_exterior = True


def test_decor_capability_required():
    with pytest.raises(CapabilityRequired):
        validate_apply_decal(
            capabilities={"canDecorateExterior": False},
            snapshot=FakeSnapshot(),
            decal=FakeDecal(),
            target={
                "panel": "door_left",
                "uv_transform": {
                    "x": 0.2,
                    "y": 0.2,
                    "scale": 1.0,
                    "rotation": 0
                }
            }
        )

