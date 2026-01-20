def test_cannot_draft_non_completed_snapshot(
    client,
    draft_snapshot,
    editor_user,
):
    res = client.post(
        f"/snapshots/{draft_snapshot.id}/draft",
        headers=auth(editor_user),
    )

    assert res.status_code == 409

