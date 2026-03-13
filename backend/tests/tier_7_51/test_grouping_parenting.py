from app.services.mutations.scene_objects import (
    apply_create_group,
    apply_parent_object,
    apply_unparent_object,
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
                    "parent_id": None,
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

def test_create_group():
    s = FakeSnap()
    r = apply_create_group(s, {"name": "Vehicle Group"})
    assert r["ok"] is True
    assert len(s.body_state["objects"]) == 2

    groups = [o for o in s.body_state["objects"] if o["kind"] == "group"]
    assert len(groups) == 1
    assert groups[0]["name"] == "Vehicle Group"

def test_parent_object():
    s = FakeSnap()
    g = apply_create_group(s, {"name": "Vehicle Group"})
    gid = g["object_id"]

    r = apply_parent_object(s, {"object_id": "obj-1", "parent_id": gid})
    assert r["ok"] is True

    car = [o for o in s.body_state["objects"] if o["id"] == "obj-1"][0]
    assert car["parent_id"] == gid

def test_unparent_object():
    s = FakeSnap()
    g = apply_create_group(s, {"name": "Vehicle Group"})
    gid = g["object_id"]
    apply_parent_object(s, {"object_id": "obj-1", "parent_id": gid})

    r = apply_unparent_object(s, {"object_id": "obj-1"})
    assert r["ok"] is True

    car = [o for o in s.body_state["objects"] if o["id"] == "obj-1"][0]
    assert car["parent_id"] is None
