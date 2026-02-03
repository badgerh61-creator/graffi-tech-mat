def test_flow_guidance_exposed(client, editor_user):
    res = client.get(
        "/studio/flow",
        headers=auth(editor_user),
    )

    assert "next_allowed_tools" in res.json()

