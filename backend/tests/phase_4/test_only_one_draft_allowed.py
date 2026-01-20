def test_only_one_draft_allowed(
    client,
    completed_snapshot,
    existing_draft_snapshot,
    editor_user,
):
    res = client.post(
        f"/snapshots/{completed_snapshot.id}/draft",
        headers=auth(editor_user),
    )

    assert res.status_code == 409

