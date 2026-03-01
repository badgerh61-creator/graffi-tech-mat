from app.services.materials.mutator import apply_set, apply_update_params

class FakeSnap:
    def __init__(self):
        self.decor_state = {}

def test_update_params_clamps_and_normalizes():
    s = FakeSnap()
    apply_set(s, {"target_id": "obj-1", "preset": "matte_black"})

    r = apply_update_params(s, {
        "target_id": "obj-1",
        "patch": {"color": "#aa11cc", "roughness": 2.0, "metalness": -1.0, "opacity": 0.5},
    })
    assert r["ok"] is True
    p = s.decor_state["material_overrides"]["obj-1"]["params"]
    assert p["color"] == "#AA11CC"
    assert p["roughness"] == 1.0
    assert p["metalness"] == 0.0
    assert p["opacity"] == 0.5
