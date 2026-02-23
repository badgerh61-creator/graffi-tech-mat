from app.services.selection_resolution import resolve_selection

def test_winner_deterministic_sort():
    r = resolve_selection(
        hit_candidates=[
            {"target_id": "panel-9", "kind": "panel", "depth": 0.1},
            {"target_id": "v-2", "kind": "vertex", "depth": 0.9},
            {"target_id": "v-1", "kind": "vertex", "depth": 0.2},
        ],
        modifiers={"shift": False, "ctrl": False},
        previous_selection={"selected_target_ids": [], "active_target_id": None},
    )
    assert r.winner == "v-1"
    assert r.selected_target_ids == ["v-1"]
    assert r.active_target_id == "v-1"
