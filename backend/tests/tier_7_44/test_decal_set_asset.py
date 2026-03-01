from app.services.decals.mutator import apply_set_asset

class FakeSnap:
    def __init__(self):
        self.decor_state = {"decals": [{"id": "dec-1", "asset_id": None, "version": 1}]}

def test_set_asset_updates_decal():
    s = FakeSnap()
    r = apply_set_asset(s, {"decal_id": "dec-1", "asset_id": "asset-flame"})
    assert r["ok"] is True
    d = s.decor_state["decals"][0]
    assert d["asset_id"] == "asset-flame"
    assert "url" in d
