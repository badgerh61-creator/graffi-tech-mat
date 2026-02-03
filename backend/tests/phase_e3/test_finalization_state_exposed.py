def test_finalization_state_exposed(
    client,
    completed_snapshot,
    editor_user,
):
    res = client.get(
        f"/studio/snapshots/{completed_snapshot.id}/state",
        headers=auth(editor_user),
    )

    data = res.json()
    assert data["status"] == "completed"
    assert data["immutable"] is True

