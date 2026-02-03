def test_block_reason_propagated(
    client,
    draft_snapshot_owned_by_other,  
    editor_user,
):
    response = client.get(
        "/studio/state",
        headers=auth(editor_user),
    )

    reason = response.json()["block_reason"]
    assert reason is not None
    assert reason["code"] == "snapshot.locked"

