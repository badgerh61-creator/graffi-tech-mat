import pytest
from app.validation.decor.exterior import validate_apply_decal
from app.validation.decor.errors import InvalidSnapshotBase


class BadSnapshot:
    status = "pending"
    is_obsolete = False
    vehicle_panels = {"door_left"}


class FakeDecal:
    is_exterior = True


def test_invalid_snapshot_status():
    with pytest.raises(InvalidSnapshotBase):
        validate_apply_decal(
            capabilities={"canDecorateExterior": True},
            snapshot=BadSnapshot(),
            decal=FakeDecal(),
            target={
                "panel": "door_left",
                "uv_transform": {
                    "x": 0.1,
                    "y": 0.1,
                    "scale": 1.0,
                    "rotation": 0
                }
            }
        )

