from app.studio.tool_registry import get_tool

def test_tool_registry_resolves_tool():
    tool = get_tool("translate")
    assert tool is not None
    assert tool.name == "translate"

