def test_no_authority_leak(client, editor_user):
    res = client.get(
        "/studio/tools",
        headers=auth(editor_user),
    )

    for tool in res.json()["tools"]:
        assert "execute" not in tool
        assert "enabled" not in tool

