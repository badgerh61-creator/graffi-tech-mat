from app.services.tool_guard import require_tool_allowed
from app.studio.stations import StudioStation

def test_tool_allowed_when_all_conditions_met(
    draft_snapshot,
    editor_capabilities,
):
    tool = require_tool_allowed(
        tool_name="translate",
        snapshot=draft_snapshot,
        station=StudioStation.geometry,
        capabilities=editor_capabilities,
    )

    assert tool.operation == "transform.translate"

