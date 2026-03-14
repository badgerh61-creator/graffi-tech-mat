from app.services.mutations.scene_objects import (
    apply_bulk_set_enabled,
    apply_bulk_set_layers,
)


class FakeSnap:
    def __init__(self):
        self.body_state = {
            "objects": [
                {"id": "obj-1", "enabled": True, "layers": ["default"], "version": 1},
                {"id": "obj-2", "enabled": True, "layers": ["default"], "version": 1},
                {"id": "obj-3", "enabled": False, "layers": ["garage"], "version": 1},
            ]
        }


def test_bulk_set_enabled():
    s = FakeSnap()
    r = apply_bulk_set_enabled(
        s,
        {
            "object_ids": ["obj-1", "obj-2"],
            "enabled": False,
        },
    )

    assert r["ok"] is True
    assert r["updated"] == 2
    assert s.body_state["objects"][0]["enabled"] is False
    assert s.body_state["objects"][1]["enabled"] is False


def test_bulk_set_layers():
    s = FakeSnap()
    r = apply_bulk_set_layers(
        s,
        {
            "object_ids": ["obj-1", "obj-3"],
            "layers": ["reference", "default"],
        },
    )

    assert r["ok"] is True
    assert r["updated"] == 2

    obj1 = next(o for o in s.body_state["objects"] if o["id"] == "obj-1")
    obj3 = next(o for o in s.body_state["objects"] if o["id"] == "obj-3")

    assert obj1["layers"] == ["default", "reference"]
    assert obj3["layers"] == ["default", "reference"]
