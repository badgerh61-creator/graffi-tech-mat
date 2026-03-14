from app.services.variants.mutator import (
    apply_save_variant,
    apply_apply_variant,
    apply_delete_variant,
)

class FakeSnap:
    def __init__(self):
        self.body_state = {
            "objects": [
                {"id": "obj-1", "enabled": True},
                {"id": "obj-2", "enabled": False},
            ]
        }
        self.decor_state = {
            "material_overrides": {
                "obj-1": {"preset": "paint_gloss_red", "params": {}, "version": 1}
            },
            "decals": [
                {"id": "dec-1", "target_id": "obj-1", "asset_id": "asset-flame"}
            ],
            "variant_sets": [],
        }

def test_save_variant():
    s = FakeSnap()
    r = apply_save_variant(s, {"name": "Red Flame"})
    assert r["ok"] is True
    assert len(s.decor_state["variant_sets"]) == 1
    v = s.decor_state["variant_sets"][0]
    assert v["name"] == "Red Flame"
    assert v["payload"]["object_enabled"]["obj-2"] is False

def test_apply_variant():
    s = FakeSnap()
    saved = apply_save_variant(s, {"name": "Red Flame"})
    vid = saved["variant_id"]

    s.decor_state["material_overrides"] = {}
    s.decor_state["decals"] = []
    s.body_state["objects"][0]["enabled"] = False
    s.body_state["objects"][1]["enabled"] = True

    r = apply_apply_variant(s, {"variant_id": vid})
    assert r["ok"] is True
    assert "obj-1" in s.decor_state["material_overrides"]
    assert len(s.decor_state["decals"]) == 1
    assert s.body_state["objects"][0]["enabled"] is True
    assert s.body_state["objects"][1]["enabled"] is False

def test_delete_variant():
    s = FakeSnap()
    saved = apply_save_variant(s, {"name": "Red Flame"})
    vid = saved["variant_id"]

    r = apply_delete_variant(s, {"variant_id": vid})
    assert r["ok"] is True
    assert r["removed"] == 1
    assert len(s.decor_state["variant_sets"]) == 0
