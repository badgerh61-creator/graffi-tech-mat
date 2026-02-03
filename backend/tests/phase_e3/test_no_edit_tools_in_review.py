def test_no_edit_tools_in_review(
    client,
    completed_snapshot,
    editor_user,
):
    res = client.get(
        "/studio/tools",
        headers=auth(editor_user),
        params={"snapshot_id": completed_snapshot.id},
    )

    tools = res.json()["tools"]
    assert all(t["availability"] == "blocked" for t in tools)

