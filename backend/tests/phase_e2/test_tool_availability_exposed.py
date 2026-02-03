def test_tool_availability_exposed(client, editor_user):
    res = client.get(
        "/studio/tools",
        headers=auth(editor_user),
    )

    tools = res.json()["tools"]
    assert any(t["tool_id"] == "translate" for t in tools)

