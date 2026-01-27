from app.services.flow_guard import require_flow_allowed

def test_transform_to_validate_allowed():
    require_flow_allowed(
        current_state="transform",
        next_tool="validate",
    )

