from app.services.materials.paint_mutator import (
    apply_apply_library_preset,
    apply_save_swatch,
    apply_apply_swatch,
    apply_delete_swatch,
)

class FakeSnap:
    def __init__(self):
        self.decor_state = {}

def test_apply_library_preset():
    s = FakeSnap()
    r = apply_apply_library_preset(s, {
        "target_id": "obj-1::Body/MainMesh::slot:BodyPaint",
        "preset": "paint_metallic_blue",
    })

    assert r["ok"] is True
    ov = s.decor_state["material_overrides"]["obj-1::Body/MainMesh::slot:BodyPaint"]
    assert ov["preset"] == "paint_metallic_blue"
    assert ov["params"]["color"] == "#1F4BA8"

def test_save_and_apply_swatch():
    s = FakeSnap()
    save = apply_save_swatch(s, {
        "name": "Custom Red",
        "color": "#AA0000",
        "finish": "gloss",
    })
    assert save["ok"] is True
    swatch_id = save["swatch_id"]

    apply_result = apply_apply_swatch(s, {
        "target_id": "obj-1",
        "swatch_id": swatch_id,
    })
    assert apply_result["ok"] is True
    ov = s.decor_state["material_overrides"]["obj-1"]
    assert ov["params"]["color"] == "#AA0000"

def test_delete_swatch():
    s = FakeSnap()
    save = apply_save_swatch(s, {
        "name": "Custom Black",
        "color": "#111111",
        "finish": "matte",
    })
    swatch_id = save["swatch_id"]

    r = apply_delete_swatch(s, {"swatch_id": swatch_id})
    assert r["ok"] is True
    assert r["removed"] == 1
