from app.services.selection_resolution import resolve_selection

def test_empty_click_clears_without_modifiers():
    r = resolve_selection(
        hit_candidates=[],
        modifiers={"shift": False, "ctrl": False},
        previous_selection={"selected_target_ids": ["a"], "active_target_id": "a"},
    )
    assert r.selected_target_ids == []
    assert r.active_target_id is None
