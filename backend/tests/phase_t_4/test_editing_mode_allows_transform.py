from app.services.mode_guard import require_mode_allows_tool

def test_editing_mode_allows_transform():
    require_mode_allows_tool(
        mode="editing",
        tool="transform",
    )

