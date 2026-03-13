from app.services.decals.mutator import apply_create

class FakeSnap:
    def __init__(self):
        self.decor_state = {}

def test_create_decal_with_asset_id():
    s = FakeSnap()

    r = apply_create(s, {
        "target_id": "obj-1::Body/PanelA",
        "asset_id": "asset-flame",
        "initial": {
            "position": {"x": 1, "y": 2, "z": 3},
            "rotation_euler": {"x": 0, "y": 90, "z": 0},
            "scale": {"x": 1.5, "y": 1.5, "z": 1.5},
            "opacity": 0.8,
            "blend": "normal",
            "z_offset": 0.001,
        },
    })

    assert r["ok"] is True
    assert len(s.decor_state["decals"]) == 1

    d = s.decor_state["decals"][0]
    assert d["asset_id"] == "asset-flame"
    assert d["target_id"] == "obj-1::Body/PanelA"
    assert d["position"]["x"] == 1
