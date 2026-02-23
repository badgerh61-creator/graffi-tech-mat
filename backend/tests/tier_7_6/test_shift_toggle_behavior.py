from app.services.selection_resolution import resolve_selection

def test_shift_toggle_behavior():
    r = resolve_selection(
        hit_candidates=[{"target_id": "b", "kind": "panel", "depth": 0.1}],
        modifiers={"shift": True},
        previous_selection={"selected_target_ids": ["a", "b"], "active_target_id": "b"},
    )
    assert r.selected_target_ids == ["a"]
    assert r.active_target_id == "a"
