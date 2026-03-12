from app.services.mutations.scene_objects import (
    apply_set_object_enabled,
    apply_set_object_layers,
    apply_remove_object,
)

class FakeSnap:
    def __init__(self):
        self.body_state = {
            "objects": [
                {
                    "id": "obj-1",
                    "kind": "model_ref",
                    "name": "Car",
                    "asset_id": "asset-vehicle-demo",
                    "transform": {
                        "pos": {"x": 0, "y": 0, "z": 0},
                        "rot": {"x": 0, "y": 0, "z": 0},
                        "scale": {"x": 1, "y": 1, "z": 1},
                    },
                    "layers": ["default"],
                    "enabled": True,
                    "version": 1,
                }
            ]
        }

def test_set_enabled():
    s = FakeSnap()
    r = apply_set_object_enabled(s, {"object_id": "obj-1", "enabled": False})
    assert r["ok"] is True
    assert s.body_state["objects"][0]["enabled"] is False

def test_set_layers():
    s = FakeSnap()
    r = apply_set_object_layers(s, {"object_id": "obj-1", "layers": ["garage", "default"]})
    assert r["ok"] is True
    assert s.body_state["objects"][0]["layers"] == ["default", "garage"]

def test_remove_object():
    s = FakeSnap()
    r = apply_remove_object(s, {"object_id": "obj-1"})
    assert r["ok"] is True
    assert len(s.body_state["objects"]) == 0
