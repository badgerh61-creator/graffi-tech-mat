from app.services.materials.mutator import (
    apply_set_object_pivot,
    apply_reset_object_pivot,
    apply_set_object_pivot_preset,
)

class FakeSnap:
    def __init__(self):
        self.body_state = {
            "objects": [
                {
                    "id": "obj-1",
                    "kind": "model_ref",
                    "name": "Car",
                    "pivot": None,
                    "transform": {
                        "pos": {"x": 0, "y": 0, "z": 0},
                        "rot": {"x": 0, "y": 0, "z": 0},
                        "scale": {"x": 1, "y": 1, "z": 1},
                    },
                    "version": 1,
                }
            ]
        }

def test_set_object_pivot():
    s = FakeSnap()
    r = apply_set_object_pivot(s, {
        "object_id": "obj-1",
        "pivot": {"x": 1, "y": 2, "z": 3},
    })

    assert r["ok"] is True
    obj = s.body_state["objects"][0]
    assert obj["pivot"] == {"x": 1.0, "y": 2.0, "z": 3.0}

def test_reset_object_pivot():
    s = FakeSnap()
    apply_set_object_pivot(s, {
        "object_id": "obj-1",
        "pivot": {"x": 1, "y": 2, "z": 3},
    })

    r = apply_reset_object_pivot(s, {"object_id": "obj-1"})
    assert r["ok"] is True
    assert s.body_state["objects"][0]["pivot"] is None

def test_set_object_pivot_preset():
    s = FakeSnap()
    r = apply_set_object_pivot_preset(s, {
        "object_id": "obj-1",
        "preset": "center",
        "pivot": {"x": 0.5, "y": 0.25, "z": -0.5},
    })

    assert r["ok"] is True
    assert s.body_state["objects"][0]["pivot"]["x"] == 0.5
