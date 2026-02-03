def test_draft_ownership_resolution(
    client,
    draft_snapshot_owned_by_other,
    editor_user,
):
    response = client.get(
        "/studio/state",
        headers=auth(editor_user),
    )

    assert response.json()["draft_ownership"] == "owned_by_other"

