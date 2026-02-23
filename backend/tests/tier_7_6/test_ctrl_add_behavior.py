from app.services.selection_resolution import resolve_selection

def test_ctrl_add_behavior():
    r = resolve_selection(
        hit_candidates=[{"target_id": "c", "kind": "panel", "depth": 0.1}],
        modifiers={"ctrl": True},
        previous_selection={"selected_target_ids": ["a", "b"], "active_target_id": "a"},
    )
    assert r.selected_target_ids == ["a", "b", "c"]
    assert r.active_target_id == "c"
