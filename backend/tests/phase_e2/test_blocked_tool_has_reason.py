def test_blocked_tool_has_reason(
    client,
    viewer_user,
):
    res = client.get(
        "/studio/tools",
        headers=auth(viewer_user),
    )

    blocked = [t for t in res.json()["tools"] if t["availability"] == "blocked"]
    assert blocked[0]["reason"]["code"] is not None

