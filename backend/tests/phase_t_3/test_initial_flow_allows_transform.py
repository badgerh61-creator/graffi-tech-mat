from app.services.flow_guard import require_flow_allowed

def test_initial_flow_allows_transform():
    require_flow_allowed(
        current_state="start",
        next_tool="transform",
    )

