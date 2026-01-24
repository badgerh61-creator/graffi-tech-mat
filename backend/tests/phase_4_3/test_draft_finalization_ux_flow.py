def test_finalize_creates_completed_snapshot(
    client,
    draft_snapshot,
    editor_user,
):
    res = client.post(
        f"/snapshots/{draft_snapshot.id}/finalize",
        headers=auth(editor_user),
    )

    assert res.status_code == 200
    assert res.json()["status"] == "completed"

