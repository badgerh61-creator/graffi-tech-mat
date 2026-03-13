from app.services.mutations.scene_objects import (
    apply_duplicate_object,
    apply_mirror_object,
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
                        "pos": {"x": 1, "y": 2, "z": 3},
                        "rot": {"x": 0, "y": 0, "z": 0},
                        "scale": {"x": 1, "y": 1, "z": 1},
                    },
                    "layers": ["default"],
                    "enabled": True,
                    "version": 1,
                }
            ]
        }

def test_duplicate_object_adds_copy_with_offset():
    s = FakeSnap()
    r = apply_duplicate_object(
        s,
        {"object_id": "obj-1", "offset": {"x": 10, "y": 0, "z": -2}},
    )

    assert r["ok"] is True
    assert len(s.body_state["objects"]) == 2

    clones = [o for o in s.body_state["objects"] if o["id"] != "obj-1"]
    assert len(clones) == 1
    clone = clones[0]

    assert clone["name"] == "Car Copy"
    assert clone["transform"]["pos"]["x"] == 11
    assert clone["transform"]["pos"]["y"] == 2
    assert clone["transform"]["pos"]["z"] == 1

def test_mirror_object_flips_selected_axis():
    s = FakeSnap()
    r = apply_mirror_object(
        s,
        {"object_id": "obj-1", "axis": "x"},
    )

    assert r["ok"] is True
    assert len(s.body_state["objects"]) == 2

    clones = [o for o in s.body_state["objects"] if o["id"] != "obj-1"]
    clone = clones[0]

    assert clone["name"] == "Car Mirror"
    assert clone["transform"]["pos"]["x"] == -1
    assert clone["transform"]["pos"]["y"] == 2
    assert clone["transform"]["pos"]["z"] == 3
