from app.services.materials.mutator import apply_set, apply_clear

class FakeSnap:
    def __init__(self):
        self.decor_state = {}

def test_set_and_clear_override():
    s = FakeSnap()
    r = apply_set(s, {"target_id": "obj-1::MeshA", "preset": "matte_black"})
    assert r["ok"] is True
    assert s.decor_state["material_overrides"]["obj-1::MeshA"]["preset"] == "matte_black"

    r2 = apply_clear(s, {"target_id": "obj-1::MeshA"})
    assert r2["ok"] is True
    assert "obj-1::MeshA" not in s.decor_state["material_overrides"]
