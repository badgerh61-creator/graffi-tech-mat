from app.services.mutations.scene_objects import apply_add_model_ref, apply_remove_object


class FakeSnap:
    def __init__(self):
        self.body_state = {"objects": []}


def test_add_model_ref_creates_object():
    s = FakeSnap()
    r = apply_add_model_ref(s, {"asset_id": 123, "name": "Vehicle"})
    assert r["ok"] is True
    assert len(s.body_state["objects"]) == 1

    o = s.body_state["objects"][0]
    assert o["kind"] == "model_ref"
    assert o["asset_id"] == 123
    assert o["name"] == "Vehicle"
    assert "transform" in o


def test_remove_object_removes():
    s = FakeSnap()
    r1 = apply_add_model_ref(s, {"asset_id": 7})
    oid = r1["object_id"]

    assert len(s.body_state["objects"]) == 1
    r2 = apply_remove_object(s, {"object_id": oid})

    assert r2["ok"] is True
    assert r2["removed"] == 1
    assert len(s.body_state["objects"]) == 0


def test_remove_object_missing_is_safe():
    s = FakeSnap()
    r = apply_remove_object(s, {"object_id": "obj-does-not-exist"})
    assert r["ok"] is True
    assert r["removed"] == 0
