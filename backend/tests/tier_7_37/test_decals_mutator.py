from app.services.decals.mutator import apply_create, apply_update, apply_delete

class FakeSnap:
    def __init__(self):
        self.decor_state = {}

def test_create_update_delete_decal_roundtrip():
    s = FakeSnap()

    r = apply_create(s, {
        "target_id": "obj-1::CarRoot",
        "asset_ref": "builtin://checker",
        "initial": {"opacity": 0.8, "blend": "normal"}
    })
    assert r["ok"] is True
    did = r["decal_id"]
    assert len(s.decor_state["decals"]) == 1
    assert s.decor_state["decals"][0]["id"] == did

    u = apply_update(s, {"decal_id": did, "patch": {"opacity": 0.2}})
    assert u["ok"] is True
    assert abs(s.decor_state["decals"][0]["opacity"] - 0.2) < 1e-6

    d = apply_delete(s, {"decal_id": did})
    assert d["ok"] is True
    assert len(s.decor_state["decals"]) == 0
