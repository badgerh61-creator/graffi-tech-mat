from app.services.materials.mutator import apply_set_slot, apply_clear_slot

class FakeSnap:
    def __init__(self):
        self.decor_state = {}

def test_set_slot_override():
    s = FakeSnap()
    r = apply_set_slot(s, {
        "target_id": "obj-1::Body/MainMesh",
        "slot_name": "BodyPaint",
        "preset": "paint_gloss_red",
    })

    assert r["ok"] is True
    key = "obj-1::Body/MainMesh::slot:BodyPaint"
    assert key in s.decor_state["material_overrides"]
    assert s.decor_state["material_overrides"][key]["preset"] == "paint_gloss_red"

def test_clear_slot_override():
    s = FakeSnap()
    apply_set_slot(s, {
        "target_id": "obj-1::Body/MainMesh",
        "slot_name": "BodyPaint",
        "preset": "paint_gloss_red",
    })

    r = apply_clear_slot(s, {
        "target_id": "obj-1::Body/MainMesh",
        "slot_name": "BodyPaint",
    })

    assert r["ok"] is True
    key = "obj-1::Body/MainMesh::slot:BodyPaint"
    assert key not in s.decor_state["material_overrides"]
